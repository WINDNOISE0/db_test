import uuid

import pytest

from clients.kafka_client.admin import create_topic
from clients.kafka_client.consumer import consume_events
from clients.kafka_client.producer import send_event

@pytest.mark.kafka
def test_send_payment_event(kafka_producer):
    send_event(kafka_producer, "payments", {"event": "payment_created", "amount": 100.50})


@pytest.mark.kafka
def test_published_event_is_consumed(kafka_producer, kafka_consumer):
    create_topic("payments")

    # trace_id делает сообщение уникальным: в топике уже могут лежать
    # события от предыдущих прогонов, нам нужно найти именно своё
    message = {
        "event": "payment_created",
        "amount": 42.50,
        "trace_id": str(uuid.uuid4()),
    }
    send_event(kafka_producer, "payments", message)

    events = consume_events(kafka_consumer, timeout_ms=5000)

    received = [e for e in events if e.get("trace_id") == message["trace_id"]]
    assert len(received) == 1
    assert received[0] == message
