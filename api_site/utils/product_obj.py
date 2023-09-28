from typing import List, Optional

import requests


class Product:
    """
    Базовый класс определяющий объект товара, который содержит различные свойства.

    Attribute:
        __list_param (tuple) : Содержит список ключей, ко которым будут извлекаться из json файла различные свойства.

    Methods:
        _price_edit(price: str) -> float: изменяет тип цены из str в float
        _product_att(attributes: dict) -> str: Получение свойства товара преобразуются в строковое значение.
        get_product_id(self) -> str: Метод возвращает id товара.
        get_store_name(self) -> str: Метод возвращает название магазина.
        get_product_title(self) -> str: Метод возвращает название продукта.
        get_product_photos(self) -> bytes: Метод возвращает фотографию товара.
        get_product_description(self) -> str: Метод возвращает описание товара.
        get_price(self) -> float: Метод возвращает стоимость товара.
        get_product_rating(self) -> float | str: Метод возвращает  рейтинг товара.
        get_shipping(self) -> str: Метод возвращает описание доставки товара.
        get_offer_page_url(self) -> str: Метод возвращает ссылку на товар.
        get_product_attributes(self) -> str: Метод возвращает характеристики товара.
        get_param_list(cls): Метод возвращает ключи свойственные этому классу.

    Notes:
        Класс предназначен для формирования списка товаров имеющие шаблонные свойства которые
        в последующем будут формировать готовые результаты запроса.
    """
    __list_params: tuple = (
        "product_id", "product_rating", 'product_title', 'product_photos', "product_description",
        "price", "shipping", "offer_page_url", 'store_name', 'product_attributes')

    def __init__(self, product_id: str,
                 product_rating: float | int | None,
                 product_title: str,
                 store_name: str,
                 product_photos: List[str],
                 product_description: str,
                 product_attributes: dict | None,
                 price: str,
                 shipping: str,
                 offer_page_url: str
                 ) -> None:

        self._product_id: str = product_id
        self._store_name: str = store_name
        self._product_title: str = product_title
        self._product_photos: List[str] = product_photos
        self._product_description: str = product_description
        self._price: float = self._price_edit(price)
        self._product_rating: float | int | Optional[None] = product_rating
        self._shipping: str = shipping
        self._offer_page_url: str = offer_page_url
        self._product_attributes: str = self._product_att(product_attributes)

    @staticmethod
    def _price_edit(price: str) -> float:
        """Метод преобразует str значение во float"""
        price_new_format: float = float(((''.join(dig for dig in price
                                                  if dig.isdigit() or dig == ',' or dig == '.'))
                                         .replace(",", '.')))
        return price_new_format

    @staticmethod
    def _product_att(attributes: dict) -> str:
        """Метод преобразует Dict значение в str"""
        if attributes:
            str_: str = ''
            for params, text in attributes.items():
                str_ += ''.join(params + ':' + text + '\n')
            return str_
        return 'Информация не доступна.'

    def get_product_id(self) -> str:
        """Метод возвращает id товара."""
        return self._product_id

    def get_store_name(self) -> str:
        """Метод возвращает название магазина."""
        return self._store_name

    def get_product_title(self) -> str:
        """Метод возвращает название товара."""
        return self._product_title

    def get_product_photos(self) -> bytes:
        """
        Метод возвращает изображение товара по ссылке, которая имеется в объекте,
        Args:
            None.

        Returns:
            bytes: Изображение товара.
        """
        with requests.get(self._product_photos[0]) as pict:
            return pict.content

    def get_link_photo(self):
        """Метод возвращает ссылку на ресурс изображения"""
        if self._product_photos:
            return self._product_photos[0]

    def get_product_description(self) -> str:
        """Метод возвращает описание товара."""
        if self._product_description:
            return self._product_description
        return 'Без данных'

    def get_price(self) -> float:
        """Метод возвращает стоимость товара."""
        return self._price

    def get_product_rating(self) -> float | str:
        """Метод возвращает рейтинг товара."""
        if self._product_rating:
            return self._product_rating
        return 'Без данных.'

    def get_shipping(self) -> str:
        """Метод возвращает описание доставки товара."""
        return self._shipping

    def get_offer_page_url(self) -> str:
        """Метод возвращает ссылку на магазин товара."""
        return self._offer_page_url

    def get_product_attributes(self) -> str:
        """Метод возвращает параметры товара."""
        if self._product_attributes:
            return self._product_attributes

    @classmethod
    def get_param_list(cls) -> tuple:
        """Метод возвращает ключи по которым будут формироваться запросы."""
        return cls.__list_params

    def __repr__(self):
        return f"{self._product_title}"


if __name__ == '__main__':
    HelloWorld = print
    HelloWorld('print')
