import os
import abc
from typing import Optional, List

import dotenv
from datetime import datetime

dotenv.load_dotenv()


class Setting(abc.ABC):
    """
    Абстрактный класс передает настройки  чувствительных данных для дальнейшего использования.
    Methods:
        get_token_tg: возвращает TOKEN_TG_API
    """
    __current_dir = os.getcwd()
    __path_of_requests_dir = os.path.abspath(os.path.join(__current_dir + '/api_site/utils/requests_files/'))
    __path_log_file = os.path.abspath(os.path.join(__current_dir + '/log/log.log'))
    __max_count_files = 1000

    @staticmethod
    def get_token_tg() -> str:
        """Метод возвращает токен тг."""
        return os.getenv('TOKEN_TG_API')

    @staticmethod
    def get_host_db():
        """ Метод предоставляет хост БД."""
        return os.getenv('HOST_BD')

    @staticmethod
    def get_user_mysql() -> str:
        """Метод предоставляет логин БД."""
        return os.getenv("USER_MYSQL")

    @staticmethod
    def get_password_mysql() -> str:
        """Метод предоставляет пароль БД."""
        return os.getenv("Password_SQL")

    @staticmethod
    def get_port_db():
        """Метод предоставляет числовое значение порта, который будет прослушиваться.
        Обычно умолчанию 3306, если не занят."""
        return int(os.getenv('PORT_DB'))

    @classmethod
    def get_path_db(cls) -> str:
        """Возвращает путь, название и расширение файла"""
        return os.getenv('NAME_DB')

    @staticmethod
    def get_api_key() -> str:
        """Передает X-RapidAPI-Key"""
        return os.getenv("X-RapidAPI-Key")

    @staticmethod
    def get_api_host() -> str:
        """Передает X-RapidAPI-Host"""
        return os.getenv("X-RapidAPI-Host")

    @classmethod
    def get_path_for_json_dir(cls) -> str:
        """Возвращает путь к кэш-файлу"""
        return cls.__path_of_requests_dir

    @classmethod
    def check_path(cls, path: str) -> bool:
        """
        Проверка файла перед его чтением.
        Returns:
            bool: В случае отсутствия файла в директории будет возвращено False, иначе True.
        """
        if os.path.exists(path):
            return True
        return False

    @classmethod
    def check_log_file(cls) -> str | Optional[None]:
        """
            Метод возвращает путь к системному файлу.
        Raises:
            OSError: Может возникнуть из-за отсутствия прав.
            FileNotFoundError: Может возникнуть из-за отсутствия директории.
        Notes:
            Метод проверяет наличие лог файла в системе, в случае он существует, возвращается
            строковое значение пути к файлу. В случае, если не обнаружен путь к файлу, будет создана
            данная директория и зачем будет создан файл в данной директории с записью о том что был создан
            новый экземпляр.
        """
        try:
            if os.path.exists(cls.__path_log_file):
                return cls.__path_log_file
            if not os.path.exists(cls.__path_log_file[:-7]):
                try:
                    os.makedirs(cls.__path_log_file[:-7])
                except OSError as er:
                    print("Не удалось создать файл log.log", er)

            with open(cls.__path_log_file, 'w', encoding="UTF-8") as file:
                file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
                           f"- Не обнаружен файл, был создан новый экземпляр.\n")
                return cls.__path_log_file
        except FileNotFoundError:
            return

    @classmethod
    def get_files_requests(cls) -> List[str]:
        """
        Метод возвращает список временных файлов.

        Returns:
             list(path_files): Вернет список с доступными данными о
             временных файлах, иначе вернет пустой список.
        """
        if os.path.exists(cls.__path_of_requests_dir):
            return os.listdir(cls.__path_of_requests_dir)
        else:
            os.makedirs(cls.__path_of_requests_dir)
            return []

    @classmethod
    def get_limit_folders(cls) -> int:
        """Метод возвращает настройки лимита временных файлов"""
        return cls.__max_count_files

    @classmethod
    def sorted_list_dir(cls, dir_list: list) -> OSError | int:
        """
        Метод для удаления временных файлов.
        Временные файлы /api_site/utils/requests/ выполняют роль кеша при обращении пользователем
        к его поисковой истории запросов к API. В случае их избыточного кол-ва часть из них будет удалена.

        Params:
            dir_list (list): список временных файлов.

        Return:
            OSError | int в случае успешной операции возвращает кол-во удаленных файлов. Иначе возвращает ошибку.

        Raise:
            OSError: в случае не успеха удаления временных файлов.

        Notes:
        Метод сортирует список временных файлов, после чего создается индекс среза.
        В данном срезе средствами цикла for происходит удаление всех файлов которые оказались внутри среза.
        В
        """
        sorted_date_files: List[str] = sorted(dir_list, key=lambda x: os.path.getatime(cls.__path_of_requests_dir))
        count: int = 0
        slice_: int = int(cls.__max_count_files * 0.6)
        for file in sorted_date_files[slice_:]:
            path: str = f'{cls.__path_of_requests_dir}/{file}'
            try:
                os.remove(path)
                count += 1
            except OSError as err:
                return err
        return count
