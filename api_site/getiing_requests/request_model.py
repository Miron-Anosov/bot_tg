from typing import TypeVar, Dict, Optional
from time import sleep
import requests
from api_site.config_get_requests.configs_base import ConfigsAPI
from common_utils.config_log import logger

T = TypeVar('T')


class ResponseAPISite:
    """
    Класс предназначен для обработки запросов к сторонним API и возвращает результат методом get_requests().
    Все параметры запроса сохраняются в конструкторе, что в дальнейшем упрощает добавления методов,
    которые могли бы оперировать с аргументами данного класса.
    Methods:
        get_requests(self) -> Response object: Возвращает результаты запросов.
    Arguments:
         self._url (str): адрес запроса.
         self._headers (dict): headers запроса хранится в модуле config.py и
            с помощью метода класса ConfigsAPI.get_headers() они передаются в данный аргумент.
         self._param (dict): Принимается арги и кварги, в зависимости от типа запроса
         и возвращает dict c обработанными параметрами.
    """

    def __init__(self, model: T, *args: str, **kwargs: Dict) -> None:
        self._url: str = ''.join(model.get_url() + model.method())
        self._headers: Dict = ConfigsAPI.get_headers()
        self._param: Dict = model.param(*args, **kwargs)

    def get_requests(self) -> requests.Response | None:
        """
        Метод возвращает Response object  извлекая данные из конструктора.
        Returns:
             The Response object | None
        """
        response = Optional[None]
        try:
            trying: int = 0
            while trying != 2:
                with requests.get(url=self._url, headers=self._headers, params=self._param) as response:
                    if response.status_code == 200:
                        return response
                    else:
                        logger.debug(f"Неудачная попытка запроса request_model.py.ResponseAPISite\n\t"
                                     f"{response.status_code=}")
                        trying += 1
                        sleep(trying * 2)
                        continue
            else:
                response.close()
                raise TimeoutError(response.status_code)
        except TimeoutError as er:
            logger.error(f"pi_site/getting_requests/request_model.py"
                         f"\n\tНет ответа от сервера: url = {self._url};"
                         f"\n\t\tparam = {self._param};"
                         f"\n\t\ter = {er}\n")
            return response
