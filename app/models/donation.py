from sqlalchemy import Column, Text, Integer, ForeignKey

from .base import FinanceBase


class Donation(FinanceBase):
    """ Класс модели Пожертвование."""
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
