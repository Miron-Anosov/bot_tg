import logging
from common_utils.config import Setting

_path = Setting.check_log_file()


def log_conf(path: str | None) -> None:
    """
    Функция применяет настройки логирования.
    Params:
     path (str): Строковое обозначения пути к файлу логирования.
    """
    logging.basicConfig(level=logging.DEBUG,
                        filename=path,  # Пуль к файлу.
                        format="%(asctime)s - %(levelname)s - "
                               "%(funcName)s: %(lineno)d - %(message)s",  # Формат сообщения.
                        datefmt="%Y-%m-%d %H:%M:%S",  # Формат временных отметок в записях.
                        encoding='utf-8',  # Кодирование записей.
                        filemode='a', )  # Дописывание к существующему файлу.


if _path:
    log_conf(_path)
else:
    logging.error(r"Не удалось получить доступ к файлу ./log/log.log")
    log_conf(_path)

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    print(_path)
    logger.debug('Debug message!!')
    logger.info('info message!!')
    logger.warning('err')
    logger.error('NEED FIX')
    logger.critical('!!!omg')
