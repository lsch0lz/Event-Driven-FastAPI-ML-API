from fastapi import APIRouter

from app.api.routes import inference, results, status

api_router = APIRouter()

api_router.include_router(inference.router)
api_router.include_router(results.router)
api_router.include_router(status.router)
