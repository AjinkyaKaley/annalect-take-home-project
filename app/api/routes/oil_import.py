from fastapi import APIRouter, Depends
from settings import settings
from typing import Any
import psycopg
import os

router = APIRouter(prefix="/oil_price", tags=["oil"])

DB_CONNSTR=os.environ.get("DATABASE_URL", None)

def get_list(conn, page_num:int, page_limit:int):
    with conn.cursor() as cur:
        query = f"""
                    SELECT * 
                    FROM 
                        commodity.oil o
                    WHERE o.origintypename = 'Country'
                    LIMIT {page_limit}
                    OFFSET {page_num}
                """
        cur.execute(query)
        return cur.fetchall()


def get_dbconn():
    PG_USER = settings.PG_USER
    PG_PASSWORD = settings.PG_PASSWORD
    PG_DATABASE = settings.PG_DATABASE

    if not PG_USER or not PG_PASSWORD or not PG_DATABASE:
        raise Exception("Invalid PG credentials, check .env file")

    conn = None
    pg_conn_str = f"postgresql://localhost:5432/{PG_DATABASE}?user={PG_USER}&password={PG_PASSWORD}"

    conn = psycopg.connect(pg_conn_str)
    try:
        yield conn
    finally:
        conn.close()

@router.get("/")
def list_items(
    page_num=int,
    page_limit=int,
    conn=Depends(get_dbconn)
) -> Any:
    return get_list(conn, page_num, page_limit)