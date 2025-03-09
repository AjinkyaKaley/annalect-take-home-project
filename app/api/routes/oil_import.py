from fastapi import APIRouter, Depends
from settings import settings
from psycopg.rows import class_row
from dataclasses import dataclass
from typing import Any
import psycopg
import os

router = APIRouter(prefix="/oil_price", tags=["oil"])

DB_CONNSTR=os.environ.get("DATABASE_URL", None)


@dataclass
class oil_data:
    year:int
    month: int
    originname: str
    origintypename: str
    destinationname: str
    destinationtypename: str
    gradename: str
    quantity: int

def get_list(filter:str, page_num:int, page_limit:int, conn):
    column_name, value = filter.split("=")
    column_name = column_name.strip()
    value = value.strip()

    with conn.cursor(row_factory=class_row(oil_data)) as cur:
        query = f"""
                    SELECT * 
                    FROM 
                        commodity.oil o
                    WHERE o.{column_name} = '{value}'
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
    filter=str,
    page_num=int,
    page_limit=int,
    conn=Depends(get_dbconn)
) -> Any:
    return get_list(filter, page_num, page_limit, conn)