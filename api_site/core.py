from typing import List
from functools import lru_cache
from api_site.utils.product_obj import Product
from api_site.common import request_product


@lru_cache(maxsize=1000)
def main(method: str, product: str, **kwargs) -> List[Product]:
    """
    Функция обрабатывает запросы по типу методов API и параметров запросов пользователя.

    Params:
        method (str): Типы запросов к API
        product (str):

    Notes:
        Функция принимает два параметра на дальнейшею обработку в другие модули.
        После чего получает результат в виде списка объектов,
        которые в свою очередь предоставляют доступ к свойствам товаров.
        Свойства:
            Название продукта (str).
            Рейтинг (float).
            Фото (webp).
            Описание товара (str).
            Свойства товара (str).
            Описание доставки (str).
            Название магазина (str).
            Cсылка на предоставленный товар (str).

    Returns:

         List[Product] : В случае удачного запроса List[Product].

         None: в случае не удачного None.
    """
    result: List[Product] = request_product(method, product, **kwargs)
    return result
