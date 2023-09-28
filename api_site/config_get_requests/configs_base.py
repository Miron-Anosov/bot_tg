from typing import AnyStr, Dict
from abc import ABC
from common_utils.config import Setting


class ConfigsAPI(ABC):
    """
    Базовый класс конфигурации запросов методов API Real-Time Product Search,.
    Methods:
        get_url(): Возвращает корневую url.
        get_headers(): Возвращает параметры headers (dict).
        method(): Необходимо переназначить. Метод возвращает строку типа запроса (str).
        param(): Необходимо переназначить.  Метод возвращает параметры (dict).
    Arguments:
        __url (str): Адрес запроса.
    Raises:
         method() -> ValueError.
         param() -> ValueError.
    Notes:
        От данного класса наследуются остальные классы для различных методов запросов.
    """

    @staticmethod
    def get_url() -> AnyStr:
        """
        Метод возвращает корневую строку запроса.
        Returns:
            str: Base url.
        """
        return "https://real-time-product-search.p.rapidapi.com"

    @staticmethod
    def get_headers() -> Dict:
        """
               Метод возвращает headers для запроса.
               Returns:
                   dict: headers API
               """
        return {"X-RapidAPI-Key": Setting.get_api_key(), "X-RapidAPI-Host": Setting.get_api_host()}

    @staticmethod
    def method() -> AnyStr:
        """
               Метод возвращает строку типа запроса.
               Returns:
                   str: method API
               """
        raise ValueError("Необходимо предварительно настроить метод.")

    @classmethod
    def param(cls, *args, **kwargs) -> Dict:
        """
               Метод возвращает параметры запроса.
               Returns:
                   dict: param API
               """
        raise ValueError("Необходимо предварительно настроить метод. Передать параметры и логику.")
