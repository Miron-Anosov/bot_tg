from typing import Dict
from api_site.config_get_requests.configs_base import ConfigsAPI


class ConfigSearch(ConfigsAPI):
    """
    Класс наследуемый от базового класса ConfigsAPI.
    Класс передает внутренние атрибуты для взаимодействия с API и обработкой результатов в последующем.
    Данный инструмент позволяет находить любые товары.
    """

    __url: str = '/search'

    @classmethod
    def method(cls) -> str:
        """
        Метод возвращает строку типа запроса.
        Returns:
            str: /search
        """
        return cls.__url

    @staticmethod
    def param(product: str, country='ru', language='ru', page: int = 2) -> Dict:
        """
        Метод возвращает параметр Get запроса.
        Params:
            product (str): Название продукта.
        Returns:
             Dict: Get param.
        """

        return {"q": f'{product.lower()}', "country": country, "language": language, "page": page}
