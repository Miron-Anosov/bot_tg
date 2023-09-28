import json
from typing import TypeVar
from api_site.config_get_requests.dict_methods import dict_methods
from common_utils.config_log import logger
from common_utils.config import Setting


T = TypeVar('T')


def request_api(model_requests: T, method: str, *param, **params) -> None:
    """
    Функция предназначения для преобразования результата запроса во временный системный файл (name.json).
    Функция принимает параметры один из которых(model_requests) инициализирует запрос url.
    Args:
        model_requests (T) : Принимает модель запроса
        method (str) : Параметр предназначен для передачи типа запроса.
        *param : Параметр предназначен для передачи параметров запроса.
        **params : Параметр предназначен для передачи параметров запроса по ключу.

    """
    config_request: T = dict_methods(method.lower())  # извлекаются модели доступных методов.
    response = model_requests(config_request, *param, **params).get_requests()  # происходит запрос к API.
    product_name: str = ''.join(i for i in param)  # обрабатывается имя запроса.
    path = ''.join(f"{Setting.get_path_for_json_dir()}/{method.lower()}_{product_name.lower()}.json")
    try:
        if response:
            with open(path, 'w', encoding='UTF-8') as file:
                response = json.loads(response.text)
                json.dump(response, file, indent=4)
        else:
            raise Exception('Результат не был получен.')
    except Exception as err:
        logger.error(f'api_site/ \n\t'
                     f'{config_request=}\n\t'
                     f'{param=}{params}\t'
                     f'{err=}\n')


if __name__ == '__main__':
    print(Setting.get_path_for_json_dir())
