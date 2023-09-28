from typing import List

from data_users import db
from datetime import datetime

from data_users.models.basemodel import BaseModel


class ManagerDB:

    @staticmethod
    def write_db_story(id_user: int, message, param: bool, sort: bool) -> None:
        """
        Метод записывает данные об активности пользователя.
        Args:
            id_user: ID пользователя
            message: данные о пользователе
            param: параметры активности
            sort: параметры активности
        Returns:
            None
        """

        date: str = datetime.now().strftime("%Y.%m.%d %H:%M")
        method: str = ''

        if param is None and sort is True:
            method: str = f'up /custom'
        elif param is None and sort is False:
            method: str = f'down /custom'
        elif param is None and sort is None:
            method: str = f'def /custom'
        elif param is False:
            method: str = f'one /low'
        elif param is True:
            method: str = f'max /high'

        data = {'link_prof': f'@{message.from_user.username}', 'name': message.from_user.first_name,
                "id_user": id_user, 'request': message.text, "date": date, "method": method}

        db.write_db_story(**data)

    @staticmethod
    def write_favorite(id_user: int, link_photo: str, about: str, link_web: str) -> None:
        """
        Метод сохраняет избранные товары.
        Сохраняет 1 запись в БД.
        Args:
            id_user: Данные пользователя
            link_photo: Ссылка на ресурс изображения.
            about: Информация о товаре.
            link_web: Страница маркетплейса.
        Returns:
            None
        """

        db.favorite_db_write(id_user=id_user, link_foto=link_photo, about=about, link_web=link_web)

    @staticmethod
    def read_favorite(id_user: int) -> List[BaseModel] | None:
        """
        Метод возвращает список избранных товаров.
        Возвращает до 100 записей из БД.
        Args:
            id_user: Данные пользователя в качестве ключа.
        Returns:
            List[BaseModel]: Данные об избранных товарах.
            В случае не успеха, будет возвращен пустой список.
        """

        favorite: List[BaseModel] = db.favorite_db_read(id_user=id_user)
        return favorite

    @staticmethod
    def read_history(id_user: int) -> List[BaseModel]:
        """
        Функция возвращает историю пользователя.
        Возвращает до 10 записей из БД.
        Args:
            id_user: Данные пользователя.
        Returns:
            List[BaseModel] | None : Данные об истории запросов пользователя.
            В случае не успеха, будет возвращен пустой список.
        """

        history: List[BaseModel] = db.read_db(id_user=id_user)
        return history

    @staticmethod
    def del_favorite(id_user: int, link: str) -> None:
        """
        Метод предназначен для удаления записей избранных товаров .
        Удаляет 1 запись из БД.
        Args:
            id_user: Данные пользователя.
            link: Ссылка на товар.

        Returns:
            None
        """

        db.del_favorite(id_user=id_user, link=link)
