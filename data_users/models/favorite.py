from peewee import ForeignKeyField, AutoField, TextField
from data_users.models.user_tg import UserTg
from data_users.models.basemodel import BaseModel


class Favorite(BaseModel):
    """
    Класс дочерний от BaseModel. Атрибуты класса создают поля в БД.

    Attribute:
        owner: Используется для создания внешнего ключа привязанный к таблице UserTg.
        link_foto: Используется для хранения ссылок на фото товара.
        about: Используется для хранения информации о товаре.
        count = AutoField(primary_key=True) Необходимо для лимита записей.
    """
    owner_favorite = ForeignKeyField(UserTg, backref='favorite')
    link_foto = TextField()
    about = TextField()
    link_web = TextField()
    ID = AutoField(primary_key=True)
