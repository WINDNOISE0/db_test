import pytest
from db.connections import get_connections

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
