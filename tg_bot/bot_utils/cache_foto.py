from typing import Dict
from api_site.utils.check_time_for_log import decorator_for_check_time
import requests


class CacheFoto:
    """
    Базовый класс, предназначен для кеширования фото.

    Attributes:
         __cache_foto: Dict: содержит временные ссылки на загруженные изображения в память.
    """
    __cache_foto: Dict = {}

    @decorator_for_check_time
    def check_cache(self, pattern: str, link: str) -> bytes:
        """
        Метод проверяет наличие ссылки в словаре. Если такая имеется в нем, то возвращает изображение.
        Иначе будет исполен get запрос, сохраним в памяти изображение и вернем его для дальнейшей обработки.

        Args:
            pattern: Необходимо для поиска в словаре данного запроса.
            link: Необходима для get запроса.

        Returns:
            bytes: Изображения.

        Notes:
            Метод снимает нагрузку с сети во время обращения пользователя к новой странице продукта.
            Что ускорит выдачу готовых результатов. В дальнейшем можно создать лимит словаря, при увеличении нагрузки.
        """

        if self.__cache_foto.get(pattern):
            pict = self.__cache_foto.get(pattern)
            return pict
        else:
            with requests.get(link) as pict:
                self.__cache_foto[pattern] = pict.content
            return pict.content
