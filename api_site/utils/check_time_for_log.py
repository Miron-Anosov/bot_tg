from typing import Callable
from time import time
from common_utils.config_log import logger
from functools import wraps


def decorator_for_check_time(func: Callable) -> Callable:
    """Декоратор предназначен для фиксирования результатов времени формирования запросов."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        stop = time() - start
        logger.info(f'затраченное время на выполнение {func} = {stop}')
        return result

    return wrapper
