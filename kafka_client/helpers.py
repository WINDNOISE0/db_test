import time

from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError


def send_event(producer, topic, message):
    producer.send(topic, value=message)
    producer.flush()


def create_topic(topic_name, num_partitions=1, replication_factor=1,
                 bootstrap_servers="localhost:9092"):
    admin = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
    try:
        admin.create_topics([
            NewTopic(
                name=topic_name,
                num_partitions=num_partitions,
                replication_factor=replication_factor,
            )
        ])
    except TopicAlreadyExistsError:
        # Идемпотентность: повторный прогон теста не должен падать
        pass
    finally:
        admin.close()


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
