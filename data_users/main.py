from data_users.models.basemodel import db
from data_users.models.favorite import Favorite
from data_users.models.history import History
from data_users.models.user_tg import UserTg
from data_users.utils.read_and_write_in_bd import WriteAndReadData

with db:
    db.create_tables([UserTg, History, Favorite])

interface = WriteAndReadData()
