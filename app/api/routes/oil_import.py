from fastapi import APIRouter, Depends, HTTPException
from models.oil_data import oil_data
from models.oil_update_record import oil_update_record
from core.db import get_dbconn
from core.queries import get_list, get_record, insert_record, check_valid_id, update_record, delete_record
from typing import Any

router = APIRouter(prefix="/oil", tags=["oil"])

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
