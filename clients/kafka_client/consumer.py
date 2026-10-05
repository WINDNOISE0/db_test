import time


def consume_events(consumer, timeout_ms=5000):
    deadline = time.monotonic() + timeout_ms / 1000
    events = []

    # Первый poll обычно уходит на присоединение к группе и возвращает пусто,
    # поэтому опрашиваем в цикле — но не дольше timeout_ms, чтобы тест
    # не завис, если сообщений в топике нет вообще
    while time.monotonic() < deadline:
        batches = consumer.poll(timeout_ms=500)
        if not batches:
            if events:
                break
            continue
        for records in batches.values():
            events.extend(record.value for record in records)

    return events
