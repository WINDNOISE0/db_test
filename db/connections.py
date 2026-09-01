import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_connections():
    return psycopg2.connect(
    host='localhost',
    port='5432',
    dbname='payments_test',
    user='test',
    password='test'
)

def get_engine():
    return create_engine("postgresql+psycopg2://test:test@localhost:5432/payments_test")

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()