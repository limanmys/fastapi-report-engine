from fastapi import APIRouter
from api.endpoints import reports, templates

api_router = APIRouter()
api_router.include_router(reports.router, tags=["Report"])
api_router.include_router(templates.router, prefix="/templates", tags=["Template"])