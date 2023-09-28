from typing import List, TypeVar, Dict, Any
from common_utils.config_log import logger

T = TypeVar('T')


def create_data_collection(data: dict, list_param: tuple, model_product: T) -> List[T] | None:
    """
    Функция возвращает коллекцию объектов наименования товаров.
    Params:
        data (dict): Словарь содержит перечень наименований товаров.
        list_param (tuple): Содержит список ключей, по которым будут извлекаться данные.
        model_product (T) : Содержит класс по которому будут формироваться объекты товаров.
    Returns:
        List[T]: Возвращает список объектов наименования найденных товаров.
    Raise:
        TypeError: Возникает, если в model_product был не верно определен list_param.
        В случае возникновения ошибки возвращен будет пустой список.
    Notes:
          Функция формирует список объектов (model_product) по предварительно переданным ключам (list_param).
          Формируется словарь, извлекаются все необходимые параметры и затем распаковываются в model_product,
          из которых в свою очередь формируется список объектов.
    """
    try:
        list_variable_products: List = []  # Пустой список для новой коллекции товаров.
        for data_product in data:
            dict_params: Dict = {}
            for key_param in list_param:  # извлекаются параметры для объекта - товара.
                value: Any = data_product.get(key_param)
                if value:
                    dict_params[key_param] = value
                else:
                    # TODO можно улучшить до рекурсивного поиска ключей.
                    value: Any = data_product["offer"].get(key_param)
                    dict_params[key_param] = value
            list_variable_products.append(model_product(**dict_params))  # распаковываем данные в новый объект.

        return list_variable_products
    except TypeError as err:
        logger.error(f"api_site/utils/read_json_file.py,\n\t"
                     "Необходимо проверить параметры которые передает list_param.\n\t"
                     "Так же проверить типы данных, которые передаются в  model_product.__init__\n\t"
                     f"{err=}")
        return []  # в случае неудачного запроса будет возвращен пустой список.
