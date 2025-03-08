from fastapi import FastAPI
from app.api.main import api_router
import os

app = FastAPI(
    title="crude oil service",
    openapi_url="/v1/openapi.json"
)

DATABASE_URL = os.environ.get("DATABASE_URL", None)
print(f"printing db {DATABASE_URL}")
app.include_router(api_router)