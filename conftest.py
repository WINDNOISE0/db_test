import pytest
from db.connections import get_connections, get_engine, get_session


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
    engine = get_engine()
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
    session = get_session(db_conn)
    yield session
    session.close()




