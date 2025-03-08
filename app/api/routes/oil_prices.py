from fastapi import APIRouter
from typing import Any


router = APIRouter(prefix="/oil_price", tags=["oil"])

@router.get("/")
def read_items(
    skip: int = 0, limit: int = 100
) -> Any:
    return