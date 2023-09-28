from typing import List
from peewee import DoesNotExist
from data_users.models.basemodel import db
from data_users.models.basemodel import BaseModel
from data_users.models.favorite import Favorite
from data_users.models.history import History
from data_users.models.user_tg import UserTg
from common_utils import logger


class WriteAndReadData:
    """
    Класс предназначен для записи в БД историю запрос пользователей.

    Methods:
        write_db (): Получает данные и записывает их.
        read_db (): Возвращает историю запросов.

    Notes:
        Класс обращается к базам данным и выполняет чтение/запись/ удаление из БД.
        В методе write_db () в случае, если это новый пользователь, создаются записи в таблице UserTg.
        В Методе read_db () в случае, если в БД хранится более 10 запросов, то часть их удаляется (Согласно ТЗ).
    """

    @staticmethod
    def write_db_story(name: str, link_prof: str, id_user: int, request: str, date: str, method: str) -> None:
        """
        Метод предназначен для создания новых записей в таблице History.

        Params:
            name (str): Имя пользователя.
            link_prof (str): Ссылка на профиль.
            id_user (int): ID профиля
            request (str): Поисковой запрос.

        Raises:
            DoesNotExist: Возникает в случае использования метода get().
            Если пользователя нет в БД, то вызывается исключение.
            После чего в блоке except будет сознана новая запись в
            таблице UserTg.
            Затем в log.log будет внесена об этом запись,
            что добавлен в БД новый пользователь.
        Notes:
            Метод первым делом проверяет наличие пользователя в БД.
            Если не отрабатывает блок except. То в БД
            добавится новая запись к закрепленному пользователю.

        Returns:
            None
        """
        with db.atomic():
            try:
                # Попытка получить пользователя из БД.
                user = UserTg.get(UserTg.id_user_tg == id_user)
                History.create(owner=user, request=request, date=date, method=method)
            except DoesNotExist:
                # Если пользователя нет, создаем новую запись.
                user = UserTg.create(id_user_tg=id_user, name=name, link_prof=link_prof)
                logger.info(f'Новый пользователь: Имя {name}, ссылка {link_prof} id {id_user}')
                History.create(owner=user, request=request, date=date, method=method)

    @staticmethod
    def read_db(id_user: int) -> List[History] | List:
        """
        Метод возвращает список запросов определенного пользователя.

        Params:
            id_user (int): ID пользователя.

        Notes:
            Метод открывает БД. После чего создается список экземпляров историй запроса.
            После этого будет произведена проверка длины списка.
            Если длина списка будет превышать допустимого лимита,
            то список будет отсортирован по уникальному значению (count).
            Из отсортированного списка будут удалены по срезу устаревшие данные.
            И в конце будет возвращен список истории пользователя.

        Returns:
            List[BaseModel]: Список содержит историю запросов писка.
        """
        with db.atomic():
            try:
                user: UserTg = UserTg.get(UserTg.id_user_tg == id_user)
                history: List[History] = History.select().where(History.owner == user).execute()
            except DoesNotExist:
                return []
            if len(history) > 10:
                history: List[History] = sorted(history, key=lambda x: x.count, reverse=True)
                for story in history[10::]:
                    # Удаление старой истории из БД.
                    story.delete_instance()
                return history[:10]
            return history

    @staticmethod
    def favorite_db_write(id_user: int, link_foto: str, about: str, link_web: str) -> None:
        """
        Метод сохраняет избранные товары в БД.
        Args:
            id_user: ID пользователя.
            link_foto: Используется для хранения ссылок на фото товара.
            about: Используется для хранения информации о товаре.
            link_web:
        Returns:

        """
        with db.atomic():
            user = UserTg.get(UserTg.id_user_tg == id_user)
            Favorite.create(owner_favorite=user, link_foto=link_foto, about=about, link_web=link_web)

    @staticmethod
    def favorite_db_read(id_user: int) -> List[BaseModel]:
        """
        Метод возвращает список сохраненных товаров.
        Args:
            id_user: ID пользователя.

        Returns:
            List[BaseModel]: Список содержит сохраненные товары.
        """
        with db.atomic():
            try:
                user: UserTg = UserTg.get(UserTg.id_user_tg == id_user)
                favorite: List[Favorite] = Favorite.select().where(Favorite.owner_favorite == user).execute()
            except DoesNotExist:
                return []
            if len(favorite) > 100:
                favorite = sorted(favorite, key=lambda x: x.count, reverse=True)
                for story in favorite[100::]:
                    # Удаление старой истории из БД.
                    story.delete_instance()
                return favorite[:100]
            return favorite

    @staticmethod
    def del_favorite(id_user: int, link: str):
        """
        Метод предназначен для удаления из БД не актуальных товаров.
        Args:
            id_user: ID пользователя.
            link: Ссылка на товар.

        Returns:
            None
        """
        with db.atomic():
            try:
                user: UserTg = UserTg.get(UserTg.id_user_tg == id_user)
                favorite = Favorite.get(Favorite.owner_favorite == user, Favorite.link_web == link)
                favorite.delete_instance()
            except Favorite.DoesNotExist:
                logger.debug(f'Не успешная попытка удалить объект из таблицы:'
                             f' {Favorite.DoesNotExist}, {id_user=}, {link=}')
