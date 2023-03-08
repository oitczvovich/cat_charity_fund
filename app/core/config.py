from typing import Optional

from pydantic import BaseSettings, EmailStr

NULL_VALUE = 0

"""Предупреждения возвращаемые при валидации."""
PROJECT_NOT_FOUND = 'Проект не найден!'
PROJECT_DUPLICATE = 'Проект с таким именем уже существует!'
PROJECT_CLOSE = 'Закрытый проект нельзя редактировать!'
WRONG_SUMM = 'Сумма не может быть меньше зачисленных: '
PROJECT_HAVE_MONYE = 'В проект были внесены средства, не подлежит удалению!'


class Settings(BaseSettings):
    app_title: str
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    description: str
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
