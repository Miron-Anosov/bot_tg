from peewee import ForeignKeyField, CharField, AutoField
from data_users.models.user_tg import UserTg
from data_users.models.basemodel import BaseModel


class History(BaseModel):
    """
    Класс дочерний от BaseModel. Атрибуты класса создают поля в БД.

    Attribute:
        owner: Используется для создания внешнего ключа привязанный к таблице UserTg.
        count: Используется для создания уникальных значений в таблице.
        request: Используется для хранения поисковых запросов.
    """
    owner = ForeignKeyField(UserTg, backref='history')
    ID = AutoField(primary_key=True)
    request = CharField(max_length=30)
    method = CharField(max_length=15, collation='utf8mb4_general_ci')
    date = CharField()
