from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crub
from app.models import CharityProject
from app.core.config import (
    NULL_VALUE,
    PROJECT_NOT_FOUND,
    PROJECT_DUPLICATE,
    PROJECT_CLOSE,
    WRONG_SUMM,
    PROJECT_HAVE_MONYE,
)


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crub.get(
        obj_id=charity_project_id, session=session
    )
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PROJECT_NOT_FOUND
        )
    return charity_project


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crub.get_project_id_by_name(
        project_name=project_name,
        session=session
    )
    if project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_DUPLICATE
        )


def check_close_project(obj):
    if obj.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_CLOSE
        )


def check_amount(obj, new_amount=None):
    invested = obj.invested_amount
    if new_amount:
        if new_amount < invested:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=f'{WRONG_SUMM}{invested}!',
            )
    elif invested > NULL_VALUE:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_HAVE_MONYE,
        )
    return obj
