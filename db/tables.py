from sqlalchemy import MetaData, Table, Column, Integer, String, Numeric, TIMESTAMP

metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String, nullable=False),
    Column('crated_at', TIMESTAMP),
)

accounts = Table(
    'accounts',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer),
    Column('balance', Numeric(12, 2)),
    Column('currency', String)
)

transactions = Table(
    'transactions',
    metadata,
    Column('id', Integer, primary_key=True),
    Column("account_id", Integer),
    Column("type", String),
    Column("amount", Numeric(12, 2)),
    Column("status", String),
    Column("created_at", TIMESTAMP),
)