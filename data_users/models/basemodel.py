from peewee import Model, MySQLDatabase
from common_utils.config import Setting
import pymysql.cursors
# Объявляются переменные необходимые для подключения к БД.
user = Setting.get_user_mysql()
password = Setting.get_password_mysql()
name_db = Setting.get_path_db()
port_db = Setting.get_port_db()
host_db = Setting.get_host_db()

#  Инициализирует подключение к БД с использованием библиотеки PyMySQL, в случае их отсутствия будут созданы.
with pymysql.connect(host=host_db, user=user, password=password,
                     charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, port=port_db) as connect:

    with connect.cursor() as cursor:  # Попытка создания БД
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {name_db}")
        connect.commit()

# Инициализирует подключение к этой базе данных с использованием библиотеки Peewee.
db = MySQLDatabase(database=name_db, user=user, password=password, port=port_db, host=host_db)


class BaseModel(Model):
    """
    Класс базовый необходимый для создания таблиц в ДБ.
    """

    class Meta:
        database = db
