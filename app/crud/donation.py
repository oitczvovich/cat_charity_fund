from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Donation, User
from app.crud.base import CRUDBase


class CRUDDonation(CRUDBase):

    async def get_by_user(
        self,
        user: User,
        session: AsyncSession,
    ) -> list[Donation]:
        """Функция возвращает юзера по его id."""
        db_donation = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return db_donation.scalars().all()

donation_crud = CRUDDonation(Donation)