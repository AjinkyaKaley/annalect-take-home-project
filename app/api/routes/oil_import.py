from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from settings import settings
from psycopg.rows import class_row
import dataclasses
from typing import Any
import psycopg
import os

router = APIRouter(prefix="/oil", tags=["oil"])

DB_CONNSTR=os.environ.get("DATABASE_URL", None)

class oil_data(BaseModel):
    year:int
    month: int
    originname: str
    origintypename: str
    destinationname: str
    destinationtypename: str
    gradename: str
    quantity: int

class oil_record(oil_data):
    id: int

def get_list(filter:str, page_num:int, page_limit:int, conn):
    column_name, value = filter.split("=")
    column_name = column_name.strip()
    value = value.strip()

    with conn.cursor(row_factory=class_row(oil_record)) as cur:
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
    with conn.cursor(row_factory=class_row(oil_record)) as curr:
        query = f"""
                    SELECT *
                    FROM
                        commodity.oil o
                    WHERE o.id = {str(id)}
                """
        curr.execute(query)
        return curr.fetchall()

def insert_record(data, conn)->int:
    with conn.cursor() as cur:
        columns = ",".join(list(data.model_dump().keys()))
        values  = tuple(map(str,data.model_dump().values()))

        query = f"""
                    INSERT INTO commodity.oil ({columns})
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                    RETURNING id
                """
        cur.execute(query, values)
        conn.commit()

        id = cur.fetchone()[0]
        return id


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

@router.put("/record")
def add_new_record(
    data: oil_data,
    conn=Depends(get_dbconn)
)->int:
    return insert_record(data, conn)