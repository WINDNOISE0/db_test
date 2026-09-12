from kafka import KafkaProducer, KafkaConsumer
import json

def get_producer():
    return KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

def get_consumer(topic, group_id="test-group"):
    return KafkaConsumer(
        topic,
        bootstrap_servers="localhost:9092",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        group_id=group_id,
        auto_offset_reset="earliest"
    )