from sqlalchemy import select, insert

from clients.db.models import User
from clients.db.tables import users, transactions, accounts


def test_users_exists(db_cur):
    db_cur.execute("SELECT email FROM users;")
    rows = db_cur.fetchall()

    assert len(rows) >= 4


def test_users_exist_core(db_engine):
    with db_engine.connect() as conn:
        query = select(users.c.email)
        result = conn.execute(query)
        rows = result.fetchall()

    assert len(rows) >= 4


def test_insert_user_core(db_conn):
    stmt = insert(users).values(email="eve1@test.com")
    db_conn.execute(stmt)

    result = db_conn.execute(select(users.c.email).where(users.c.email == "eve1@test.com"))
    row = result.fetchone()

    assert row is not None
    assert row.email == "eve1@test.com"




def test_alice_transactions_core(db_engine):
    query = (
        select(users.c.email, transactions.c.type, transactions.c.amount)
        .select_from(users)
        .join(accounts, users.c.id == accounts.c.user_id)
        .join(transactions, accounts.c.id == transactions.c.account_id)
        .where(users.c.email == "alice@test.com")
    )

    with db_engine.connect() as conn:
        rows = conn.execute(query).fetchall()

    assert len(rows) == 2


def test_alice_transactions_isolated(db_conn):
    # Setup — тест сам создаёт нужные данные
    user_id = db_conn.execute(
        insert(users).values(email="isolated_test@test.com").returning(users.c.id)
    ).scalar()

    account_id = db_conn.execute(
        insert(accounts).values(user_id=user_id, balance=0, currency="USD").returning(accounts.c.id)
    ).scalar()

    db_conn.execute(
        insert(transactions).values(account_id=account_id, type="deposit", amount=100, status="success")
    )

    # Действие/проверка
    query = (
        select(users.c.email, transactions.c.type, transactions.c.amount)
        .select_from(users)
        .join(accounts, users.c.id == accounts.c.user_id)
        .join(transactions, accounts.c.id == transactions.c.account_id)
        .where(users.c.email == "isolated_test@test.com")
    )
    rows = db_conn.execute(query).fetchall()

    assert len(rows) == 1
    assert rows[0].amount == 100


def test_alice_transactions_orm(db_session):
    user = db_session.query(User).filter(User.email == "alice@test.com").first()
    transactions = [t for account in user.accounts for t in account.transactions]

    assert len(transactions) >= 1