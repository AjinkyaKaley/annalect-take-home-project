from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from settings import settings
from psycopg.rows import class_row
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

class oil_update_record(BaseModel):
    year: Optional[int] 
    month: Optional[int]
    originname: Optional[str]
    origintypename: Optional[str]
    destinationname: Optional[str]
    destinationtypename: Optional[str]
    gradename: Optional[str]
    quantity: Optional[int]

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
    
def check_valid_id(id: int, conn):
    query = """
                SELECT EXISTS (
                    SELECT 1
                    FROM commodity.oil
                    WHERE id=%s
                )
            """
    with conn.cursor() as cur:
        params = [id]
        cur.execute(query, params)
        return cur.fetchone()[0]

def update_record(id, data, conn):
    data = data.model_dump()
    update_col_values = []
    values = []
    for k,v in data.items():
        if v is not None:
            update_col_values.append(f"{k}=%s")
            values.append(v)

    values.append(id)
    update_cols = ",".join(update_col_values)

    query = f"""
                UPDATE commodity.oil
                SET {update_cols}
                WHERE id = %s
            """

    with conn.cursor() as cur:
        cur.execute(query, values)
        conn.commit()

        return get_record(id, conn)
    
def delete_record(id:int, conn):
    query = """
            DELETE FROM commodity.oil
            WHERE id=%s; 
            """
    values = [id]

    with conn.cursor() as cur:
        cur.execute(query, values)
        conn.commit()


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
    if not check_valid_id(id, conn):
        raise HTTPException(400, "Invalid id")
    return get_record(id, conn)

@router.put("/record")
def add_new_record(
    data: oil_data,
    conn=Depends(get_dbconn)
)->int:
    return insert_record(data, conn)

@router.patch("/record/{id}")
def update_full_record(
    id: int,
    data: oil_update_record,
    conn=Depends(get_dbconn)
):
    if not check_valid_id(id, conn):
        raise HTTPException(400, "Invalid id")

    return update_record(id, data, conn)

@router.delete("/record/{id}")
def delete_full_record(
    id: int,
    conn=Depends(get_dbconn)
):
    if not check_valid_id(id, conn):
        raise Exception(400, "Invalid id")
    
    delete_record(id, conn)
    return "Successful"
