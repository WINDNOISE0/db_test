import os

import pytest
from dotenv import load_dotenv

from clients.api.payment_client import PaymentClient
from connections import get_connections, get_engine_alchemy, get_session_alchemy, get_producer, get_consumer

pytest_plugins = ["fixtures.ui", "fixtures.auth"]
load_dotenv()

@pytest.fixture
def db_con():
    con = get_connections()
    yield con
    con.close()

@pytest.fixture
def db_cur(db_con):
    cur = db_con.cursor()
    yield cur
    cur.close()

@pytest.fixture
def db_engine():
    engine = get_engine_alchemy()
    yield engine
    engine.dispose()

@pytest.fixture
def db_conn(db_engine):
    conn = db_engine.connect()
    trans = conn.begin()
    yield conn
    trans.rollback()
    conn.close()

@pytest.fixture
def db_session(db_conn):
    # Сессия привязана к уже открытой транзакции db_conn — ORM-тесты
    # откатываются тем же rollback, что и Core-тесты
    session = get_session_alchemy(db_conn)
    yield session
    session.close()


@pytest.fixture
def kafka_producer():
    producer = get_producer()
    yield producer
    producer.close()

@pytest.fixture
def kafka_consumer():
    consumer = get_consumer(topic="payments")
    yield consumer
    consumer.close()

@pytest.fixture(scope="session")
def payment_client():

    base_url = os.getenv("PAYMENTS_BASE_URL")
    if not base_url:
        pytest.fail("PAYMENTS_BASE_URL не задан. Проверь .env")

    client = PaymentClient(base_url)

    yield client

    client.close()



