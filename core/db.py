from settings import settings
import psycopg

def get_dbconn():
    PG_USER = settings.PG_USER
    PG_PASSWORD = settings.PG_PASSWORD
    PG_DATABASE = settings.PG_DATABASE
    PG_HOSTNAME = settings.PG_HOSTNAME

    if not PG_USER or not PG_PASSWORD or not PG_DATABASE:
        raise Exception("Invalid PG credentials, check .env file")

    conn = None
    pg_conn_str = f"postgresql://{PG_HOSTNAME}:5432/{PG_DATABASE}?user={PG_USER}&password={PG_PASSWORD}"
    print(f"connection string = {pg_conn_str}")

    conn = psycopg.connect(pg_conn_str)
    try:
        yield conn
    finally:
        conn.close()
    