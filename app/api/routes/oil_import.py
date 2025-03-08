from fastapi import APIRouter
from typing import Any
import os

router = APIRouter(prefix="/oil_price", tags=["oil"])

@router.get("/")
def list_items() -> Any:
    return os.environ.get("DATABASE_URL", None)