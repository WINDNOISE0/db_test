import os
import subprocess

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def classify_failure(error_text: str) -> str:
    prompt = f"""Ты помогаешь классифицировать причину падения автотеста.
Определи категорию по тексту ошибки. Ответь ОДНИМ словом, без пояснений: BUG, FLAKY или ENVIRONMENT.

BUG — ошибка в коде продукта или в самом тесте. Сюда входят: неверная бизнес-логика, нарушение ограничений БД (unique, foreign key) из-за того, что тест не изолирован и не откатывает свои изменения, неверные assert.
FLAKY — тест нестабилен, ошибка связана с таймингом/race condition, проходит при повторном запуске без изменений в коде.
ENVIRONMENT — окружение физически недоступно: сеть, БД/сервис не запущены, отсутствует нужная зависимость/пакет, нет прав доступа.

Примеры:
"connection refused: could not connect to server" → ENVIRONMENT
"ModuleNotFoundError: No module named 'pytest'" → ENVIRONMENT
"psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint" → BUG
"AssertionError: expected status 200, got 500 — endpoint always fails" → BUG
"AssertionError: passed on retry 2/3" → FLAKY

Текст ошибки:
{error_text}
"""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=10,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text.strip()


def check_service_status():
    result = subprocess.run(
        ["docker", "compose", "ps", "--format", "json"],
        capture_output=True, text=True
    )
    return result.stdout or "no containers running"


def classify_failure_with_tools(error_text: str) -> str:
    messages = [{"role": "user", "content": f"""Классифицируй ошибку теста: BUG, FLAKY или ENVIRONMENT.
    Если не уверен, доступна ли инфраструктура — проверь через check_service_status.
    ВАЖНО: твой самый последний ответ должен содержать ТОЛЬКО одно слово (BUG, FLAKY или ENVIRONMENT), без каких-либо пояснений.

    Текст ошибки:
    {error_text}"""}]

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        tools=tools,
        messages=messages,
    )

    if response.stop_reason == "tool_use":
        tool_use_block = next(b for b in response.content if b.type == "tool_use")
        tool_result = check_service_status()

        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use_block.id,
                    "content": tool_result,
                },
                {
                    "type": "text",
                    "text": "Теперь дай финальный ответ. ОДНИМ словом: BUG, FLAKY или ENVIRONMENT. Без пояснений."
                }
            ]
        })

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=20,
            tools=tools,
            messages=messages,
        )
    elif response.stop_reason != "end_turn":
        raise ValueError(f"Unexpected stop_reason: {response.stop_reason}")

    final_text = next(b.text for b in response.content if b.type == "text")
    return final_text.strip()


def classify_failure_with_reasoning(error_text: str) -> str:
    prompt = f"""Ты помогаешь классифицировать причину падения автотеста.
Определи категорию по тексту ошибки: BUG, FLAKY или ENVIRONMENT.

BUG — ошибка в коде продукта или в самом тесте. Сюда входят: неверная бизнес-логика, нарушение ограничений БД (unique, foreign key) из-за того, что тест не изолирован и не откатывает свои изменения, неверные assert.
FLAKY — тест нестабилен, ошибка связана с таймингом/race condition, проходит при повторном запуске без изменений в коде.
ENVIRONMENT — окружение физически недоступно: сеть, БД/сервис не запущены, отсутствует нужная зависимость/пакет, нет прав доступа.

Примеры:
"connection refused: could not connect to server" → ENVIRONMENT
"ModuleNotFoundError: No module named 'pytest'" → ENVIRONMENT
"psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint" → BUG
"AssertionError: expected status 200, got 500 — endpoint always fails" → BUG
"AssertionError: passed on retry 2/3" → FLAKY

Ответь в формате: КАТЕГОРИЯ — краткое обоснование одним предложением.

Текст ошибки:
{error_text}
"""
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text.strip()


def judge_classification(error_text: str, model_answer: str) -> bool:
    judge_prompt = f"""Ты — судья, который проверяет качество классификации ошибки теста.

Текст ошибки: {error_text}
Ответ модели: {model_answer}

Критерии правильного ответа:
1. Категория (BUG/FLAKY/ENVIRONMENT) должна быть верной по смыслу ошибки
2. Обоснование должно логически соответствовать категории, а не быть общей отговоркой

Ответь ОДНИМ словом: PASS, если ответ соответствует критериям, или FAIL, если нет.
"""
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=5,
        messages=[{"role": "user", "content": judge_prompt}]
    )
    return response.content[0].text.strip() == "PASS"