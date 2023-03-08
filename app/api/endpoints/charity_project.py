from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists,
    check_name_duplicate,
    check_close_project,
    check_amount
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crub
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investments import investment

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """Запрос обрабатывается от всех пользователей."""
    return await charity_project_crub.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    if charity_project.name:
        await check_name_duplicate(
            project_name=charity_project.name,
            session=session
        )
    new_charity_project = await charity_project_crub.create(
        charity_project, session
    )
    new_charity_project = await investment(
        session,
        new_charity_project,
    )
    return new_charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_charity_project_exists(
        project_id,
        session
    )
    project = check_amount(project)
    project = await charity_project_crub.remove(
        project,
        session
    )
    return project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_projects(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    if obj_in.name:
        await check_name_duplicate(
            project_name=obj_in.name,
            session=session
        )
    project = await check_charity_project_exists(
        project_id,
        session
    )
    check_close_project(project)
    project = check_amount(project, obj_in.full_amount)
    project = await charity_project_crub.update(
        project,
        obj_in,
        session
    )
    return project
