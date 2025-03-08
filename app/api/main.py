from fastapi import APIRouter

from app.api.routes import oil_prices

api_router = APIRouter()
api_router.include_router(oil_prices.router)
