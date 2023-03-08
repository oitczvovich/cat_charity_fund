from fastapi import APIRouter

from app.api.endpoints import (
    donation_router,
    charity_projects_router,
    user_router
)

main_router = APIRouter()
main_router.include_router(
    donation_router, prefix='/donation', tags=['Donation']
)
main_router.include_router(
    charity_projects_router, prefix='/charity_project', tags=['Projects']
)
main_router.include_router(user_router)
