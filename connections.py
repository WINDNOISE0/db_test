import json

import psycopg2
from kafka import KafkaProducer, KafkaConsumer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


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

def get_connections():
    return psycopg2.connect(
    host='localhost',
    port='5432',
    dbname='payments_test',
    user='test',
    password='test'
)

def get_engine_alchemy():
    return create_engine("postgresql+psycopg2://test:test@localhost:5432/payments_test")

def get_session_alchemy(engine):
    Session = sessionmaker(bind=engine)
    return Session()