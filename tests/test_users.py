def test_users_exists(db_cur):
    db_cur.execute("SELECT email FROM users;")
    rows = db_cur.fetchall()

    assert len(rows) >= 4