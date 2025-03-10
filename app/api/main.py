from fastapi import APIRouter

from app.api.routes import oil

api_router = APIRouter()
api_router.include_router(oil.router)
