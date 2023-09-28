from typing import Dict, TypeVar
from api_site.config_get_requests.config_search import ConfigSearch

T = TypeVar('T')

# названия ключей приведены все в нижний регистр.
_config_methods: Dict = {'поиск товара': ConfigSearch, 'новые методы': None}


def dict_methods(model_: str) -> T:
    """
        При обращении к функции, она возвращает объект,
        который будет использован для работы с модулем request_api.py
        Params:
            model_ (str): Название метода API
        Returns:
            T: Модель обращения к API
        Notes:
            C добавлением новых моделей обращений к различным API.
            Данный функция вынесена в отдельный модуль, для соблюдения структурного порядка в коде.
    """
    model: T = _config_methods.get(model_)
    return model
