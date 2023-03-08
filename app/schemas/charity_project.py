from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator


class CharityProjectBase(BaseModel):
    """ Базовая схема для проекта."""
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    @validator('name')
    def name_is_empty(cls, name: str):
        if name.isspace() or name == '' or name is None:
            raise ValueError('Имя проект не может быть пустым')
        return name

    @validator('description')
    def description_is_empty(cls, description: str):
        if description.isspace() or description == '' or description is None:
            raise ValueError('Имя проект не может быть пустым')
        return description

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    """Схема для создания проекта."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    """Схема для обновления проекта."""
    pass


class CharityProjectDB(CharityProjectBase):
    """Схема с данными из БД."""
    id: int
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
