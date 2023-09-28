import json
from typing import TypeVar, List
from api_site.utils.product_obj import Product
from api_site.utils.read_json_file import create_data_collection
from api_site.utils.request_api import request_api
from api_site.utils.check_time_for_log import decorator_for_check_time
from api_site.getiing_requests.request_model import ResponseAPISite
from common_utils.config import Setting

T = TypeVar('T')


class CallSiteAPI:
    """
    Общий класс для обработки запросов различных методов API.
    """
    __path: str = Setting.get_path_for_json_dir()

    @staticmethod
    def api_site_call_create_data(method: str, *param, **params) -> None:
        """
        Метод создает запрос впоследствии чего создается файл .json для обработки дальнейшими методами.
        Params:
            method: Тип запроса (str).
            param : Параметр запроса (str).
            params : Dict
        """
        request_api(ResponseAPISite, method, *param, **params)

    @classmethod
    def get_list_obj_with_product(cls, method, product) -> List | None:
        """
        Метод возвращает список объектов с наименованием товаров.
        В случае не успеха возвращает None.
        """
        file_name: str = ''.join(f"{method}_{product}").lower()
        path: str = f'{cls.__path}/{file_name}.json'
        if Setting.check_path(path):
            with open(path, 'r', encoding='UTF-8') as file:
                data_json = json.load(file)
                objects_product_list = create_data_collection(data_json.get('data'), Product.get_param_list(), Product)
            return objects_product_list


@decorator_for_check_time
def request_product(method: str, product: str, **kwargs) -> List[Product] | None:
    """
    Функция выполняет запросы пользователя, если запрос первый, то запрос идет с API,
    Иначе извлекает данные из файла и отправляет готовый результат.
    Params:
        method: Метод запроса (str).
        product: Цель запроса (str).
    Return:
        List object products (List) | None.
    """

    list_obj_products: List[Product] | None = CallSiteAPI().get_list_obj_with_product(method, product)
    if list_obj_products:
        return list_obj_products
    else:
        CallSiteAPI().api_site_call_create_data(method, product, **kwargs)
        list_obj_products: List[Product] | None = CallSiteAPI().get_list_obj_with_product(method, product)
        return list_obj_products
