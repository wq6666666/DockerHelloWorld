from fastapi import APIRouter
from routers import news

api_router = APIRouter()
api_router.include_router(news.router)