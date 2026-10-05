import pytest

from ai_tools.triage import classify_failure, classify_failure_with_reasoning, judge_classification

EVAL_CASES = [
    # (текст ошибки, ожидаемая категория)
    ("requests.exceptions.ConnectionError: Failed to establish a new connection: [Errno 111] Connection refused", "ENVIRONMENT"),
    ("ModuleNotFoundError: No module named 'pytest'", "ENVIRONMENT"),
    ("docker.errors.DockerException: Error while fetching server API version", "ENVIRONMENT"),
    ("sqlalchemy.exc.OperationalError: could not translate host name \"postgres\" to address", "ENVIRONMENT"),

    ("AssertionError: expected status 200, got 500 — server always returns wrong status code for this endpoint", "BUG"),
    ("psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint \"users_email_key\"", "BUG"),
    ("TypeError: unsupported operand type(s) for +: 'int' and 'str'", "BUG"),
    ("AssertionError: expected 4 users in database, got 3 — seed data missing one row", "BUG"),

    ("AssertionError: passed on retry 2/3 — test occasionally times out waiting for element to appear", "FLAKY"),
    ("selenium.common.exceptions.StaleElementReferenceException: element is not attached to the page document", "FLAKY"),
    ("AssertionError: expected 5 rows, got 4 — race condition, background job hadn't finished writing yet", "FLAKY"),
]

def test_classify_failure_accuracy():
    correct = 0
    results = []

    for error_text, expected in EVAL_CASES:
        actual = classify_failure(error_text)
        is_correct = actual == expected
        correct += is_correct
        results.append((error_text[:50], expected, actual, is_correct))

    accuracy = correct / len(EVAL_CASES)

    print(f"\nAccuracy: {accuracy:.0%} ({correct}/{len(EVAL_CASES)})")
    for text, expected, actual, ok in results:
        status = "✓" if ok else "✗"
        print(f"{status} expected={expected:<12} got={actual:<12} | {text}")

    assert accuracy >= 0.7, f"Accuracy {accuracy:.0%} below threshold 70%"

@pytest.mark.llm
def test_classification_reasoning_quality():
    error = 'psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "users_email_key"'
    answer = classify_failure_with_reasoning(error)
    assert judge_classification(error, answer), f"Judge rejected answer: {answer}"