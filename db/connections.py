import psycopg2

def get_connections():
    return psycopg2.connect(
    host='localhost',
    port='5432',
    dbname='payments_test',
    user='test',
    password='test'
)

