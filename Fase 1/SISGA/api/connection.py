import psycopg2

def get_conn():
    conn = psycopg2.connect(
        host='postgres',
        port='5432',
        database='postgres',
        user='postgres',
        password='postgres'
    )
    return conn