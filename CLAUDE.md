# QA Automation Pet Framework (db_test)

## Стек
- Python, pytest
- SQLAlchemy Core (не ORM — для контроля над генерируемым SQL)
- PostgreSQL — поднимается через `docker compose up -d`
- Redpanda (Kafka-совместимый) — для практики event-driven тестирования
- Claude API — для AI-triage упавших тестов (`ai_tools/triage.py`)

## Структура проекта
- `db/` — низкоуровневый слой: `connections.py` (подключения), `tables.py` (SQLAlchemy Core таблицы), `models.py` (ORM-модели, используются только для сравнения подходов)
- `db_helpers/` — кастомный helper-слой поверх Core для тестов (предпочтительный способ работы с БД в тестах, а не прямой Core/ORM в каждом тесте)
- `ai_tools/` — AI-инструменты для тестирования (triage, генерация тест-кейсов)
- `tests/` — сами тесты

## Правила тестирования
- Все тесты, работающие с БД, используют паттерн rollback: транзакция открывается в fixture (`conn.begin()`), тест исполняет запросы, fixture делает `rollback()` после теста — никогда не коммитить изменения внутри теста напрямую
- Новую логику работы с БД добавлять в `db_helpers/`, а не размазывать сырой SQLAlchemy Core по тестам
- `.env` содержит `ANTHROPIC_API_KEY` — не коммитить, должен быть в `.gitignore`

## Запуск
- Поднять окружение: `docker compose up -d`
- Прогнать тесты: `pytest -v`
- Зайти в БД руками: `docker compose exec postgres psql -U test -d payments_test`

## AI-инструменты
- `ai_tools/triage.py` — классификация причин падения тестов (BUG/FLAKY/ENVIRONMENT) через LLM API. Сейчас использует mock вместо реального вызова — см. `_mock_llm_call` 