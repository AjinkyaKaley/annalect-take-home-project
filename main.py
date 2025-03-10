from fastapi import FastAPI
from app.api.main import api_router

app = FastAPI(
    title="commodity data service",
    openapi_url="/v1/openapi.json"
)

app.include_router(api_router, prefix="/commodity")