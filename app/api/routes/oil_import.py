from fastapi import APIRouter, Depends
from settings import settings
from psycopg.rows import class_row
from dataclasses import dataclass
from typing import Any
import psycopg
import os

router = APIRouter(prefix="/oil", tags=["oil"])

DB_CONNSTR=os.environ.get("DATABASE_URL", None)


@dataclass
class oil_data:
    id: int
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

def get_record(id, conn):
    with conn.cursor(row_factory=class_row(oil_data)) as curr:
        query = f"""
                    SELECT *
                    FROM
                        commodity.oil o
                    WHERE o.id = {str(id)}
                """
        curr.execute(query)
        return curr.fetchall()
    
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

@router.get("/")
def list_items(
    filter=str,
    page_num=int,
    page_limit=int,
    conn=Depends(get_dbconn)
) -> Any:
    return get_list(filter, page_num, page_limit, conn)

@router.get("/record/{id}")
def get_record_by_id(
    id: int,
    conn=Depends(get_dbconn)
)->Any:
    return get_record(id, conn)