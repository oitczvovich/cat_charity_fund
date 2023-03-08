from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationBase, DonationUserDB
from app.services.investments import investment

router = APIRouter()


@router.get(
    '/',
    dependencies=[Depends(current_superuser)],
    response_model=List[DonationUserDB],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.\n
    Возвращает список всех пожертвований.
    """
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=DonationUserDB,
    response_model_exclude_none=True,
    response_model_exclude={
       "user_id", "invested_amount", "fully_invested",
    }
)
async def create_donation(
    obj_in: DonationBase,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),

):
    """Любой зарегистрированный пользователь может сделать пожертвование."""
    new_donation = await donation_crud.create(obj_in, session, user)
    new_donation = await investment(
        session,
        new_donation,
    )
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationUserDB],
    response_model_exclude={
        'user_id', 'invested_amount', 'fully_invested'
    }
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Показывает все пожертвования текущего пользователя."""
    return await donation_crud.get_by_user(user, session)
