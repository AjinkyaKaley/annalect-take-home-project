from fastapi import APIRouter, Depends, HTTPException, Query, Path
from pydantic import AfterValidator
from models.oil_data import oil_data
from models.oil_update_record import oil_update_record
from core.db import get_dbconn
from core.queries import get_list, get_record, insert_record, check_valid_id, update_record, delete_record
from typing import Any, Annotated

router = APIRouter(prefix="/oil", tags=["oil"])

def validate_page_num(page_num: int):
    if page_num < 0:
        raise ValueError("page num cannot be negative")
    return page_num

@router.get("/")
def list_items(
    column_filter : Annotated[
        str, 
        Query(
            description="filter by query, format: column_name=filter_parameter",
            pattern="^([^=]+)=([^=]+)$"
        )] = "origintypename=Country",
    page_num : Annotated[
        int, 
        AfterValidator(validate_page_num)
        ]= 0,
    page_limit : Annotated[int, Query(description="page size")] = 10,
    conn=Depends(get_dbconn)
) -> Any:
    
    colname, filter = column_filter.split("=")
    return get_list(colname, filter, page_num, page_limit, conn)

@router.get("/record/{id}")
def get_record_by_id(
    id: Annotated[
        int, 
        Path(title="Id of the record", gt=0)
        ],
    conn=Depends(get_dbconn)
)->Any:
    if not check_valid_id(id,conn):
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
    id: Annotated[
        int,
        Path(title="Id of the record",gt=0)
        ],
    data: oil_update_record,
    conn=Depends(get_dbconn)
):
    if not check_valid_id(id, conn):
        raise HTTPException(400, "Invalid id")

    return update_record(id, data, conn)

@router.delete("/record/{id}")
def delete_full_record(
    id: Annotated[
        int,
        Path(title="Id of the record", gt=0)
    ],
    conn=Depends(get_dbconn)
):
    if not check_valid_id(id, conn):
        raise Exception(400, "Invalid id")
    
    delete_record(id, conn)
    return "Successful"
