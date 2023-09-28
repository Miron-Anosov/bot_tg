from typing import List

from common_utils.config import Setting
from common_utils.config_log import logger


def check_status_cache_of_files() -> None:
    """
    Функция предназначена для работы с временными файлами.

    Notes:
        Функция проверяет кол-во временных файлов.
        В случае, если их кол-во превышает установленных лимитов в Setting.get_limit_folders(),
        будет вызван метод Setting.sorted_list_dir(list_dir).
        После чего в журнал логирования будет внесена запись об совершенной оперции.
    Returns:
        None
    """
    list_dir: List[str] = Setting.get_files_requests()
    max_count: int = Setting.get_limit_folders()
    if len(list_dir) < max_count:
        return
    else:
        result = Setting.sorted_list_dir(list_dir)
        if result is int:
            logger.info(f"Из папки api_site/utils/requests были удалены временные файлы в кол-ве: {result}")
        else:
            logger.error(f'Возникла непредвиденная ошибка при удалении файлов. \n\t{result}')


if __name__ == '__main__':
    check_status_cache_of_files()
