from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, Extra


class DonationBase(BaseModel):
    """Базовая схема для создания пожертвований."""
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationUserDB(DonationBase):
    """Схема с данными из БД."""
    id: int
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    create_date: Optional[datetime]
    user_id: Optional[int]

    class Config:
        orm_mode = True
