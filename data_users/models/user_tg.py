from peewee import IntegerField, CharField, AutoField

from data_users.models.basemodel import BaseModel


class UserTg(BaseModel):
    """
    Класс дочерний от BaseModel. Атрибуты класса создают поля в БД.

    Attribute:
        ID: Уникальный номер пользователя в таблице.
        id_user_tg: Уникальный ID телеграмма.
        name: Имя пользователя.
        link_prof: Ссылка на профиль.
    """
    ID = AutoField(primary_key=True)
    id_user_tg = IntegerField()
    name = CharField()
    link_prof = CharField()
