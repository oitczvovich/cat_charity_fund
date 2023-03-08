from sqlalchemy import Column, String, Text

from .base import FinanceBase


class CharityProject(FinanceBase):
    """ Класс модели Проекты."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
