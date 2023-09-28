from typing import IO, List, Dict, Optional
import telebot
from telebot import types
import random

from api_site.utils.product_obj import Product
from common_utils import Setting
from api_site import main as get_api
from common_utils import logger
from data_users.models.history import History
from tg_bot.bot_utils.bot_data import get_text_help, get_text_about, create_date_favorite
from tg_bot.bot_utils.cache_foto import CacheFoto
from tg_bot.bot_utils.read_pattern_util import read_pattern
from tg_bot.bot_utils.manager_db_util import ManagerDB


class Bot:
    """
    Основной класс, который работает с библиотекой PyTeleBotAPI.
    Необходима для запуска бота c помощью метод run().

    Attributes:
        __text_help (str): Текстовое сообщение меня "Помощь".
        __about_text (str): Текстовое сообщение в меню "о боте".
        bot : Класс библиотеки telebot

    Methods:
         start_menu(): Стартовое меню, выводится на экран в качестве приветствия и короткой информации.
         main_menu(): Основное меню бота из которого доступен весь функционал.
         main_click_menu(): Отвечает за ориентацию в интерфейсе меню бота.
         history_menu(): Отвечает за предоставление информации о запросах.
         helper(): Предоставляет информации о главных командах.
         next_menu_for_custom_request(): Отвечает за ориентацию в "/custom" меню.
         input_search_supplies_menu(): Предоставляет пользователю ввод данных.
         check_text_for_requests_menu(): Проверяет пользовательские данные ввода.
         result_price_menu(): Выводит результаты и предоставляет интерфейс ориентации в меню.
         learn_result(): Отвечает за ориентацию в меню вывода информации.
         product_search_menu(): "/custom" меню.
         about_menu(): Меню предоставляет более подробную информацию о возможностях бота в отличии от "/help".
         run(): Отвечает за запуск бота и с помощью методов, которые находятся непосредственно в нем,
         перехватывает основные команды пользователя.
    Notes:
        Класс представляет структуру данных, которая выполняет роль обработки пользовательской информации, ее вывода
            и интерфейс взаимодействия с пользователем.
            При использовании данного класса используются модули, которые отвечают за сбор и хранение информации об
            пользовательской активности в базе данных SQLite3 используя ORM peewee для взаимодействия с нею.
            Так же задействованы модули, которые обрабатывают пользовательские запросы с API сайта.
             И с помощью интерфейса данного класса выводятся результаты запроса пользователю
             на экран в приложении телеграмм, непосредственно в интерфейсе самого бота.
    """
    __text_help: str = get_text_help()
    __about_text: str = get_text_about()

    def __init__(self) -> None:
        """
            Params:
                bot: Объект бота
                data: Dict: Данные запросов пользователей.
                page: Dict: Индексы страниц пользователей.
                param: bool: С помощью данного параметра определяется какой вывод данных необходимо совершить.
                sort: bool: С помощью данного параметра определяется тип сортировки данных.
                cache_foto: Хранить временно подгруженные фото в кеше.
                favorite_dict: Dict: Данные сохраненных товаров пользователей.
        """

        self.bot = telebot.TeleBot(Setting.get_token_tg())
        self.data: Dict = {}
        self.page: Dict = {}
        self.param: Dict = {}
        self.sort: Dict = {}
        self.favorite_dict_cache: Dict = {}
        self.cache_foto = CacheFoto()
        self.favorite_dict: Dict = {}

    def start_menu(self, message: telebot.types.Message) -> None:
        """
        Метод используется при первом запуске бота для приветствия и короткого ознакомления.
        """
        text_output: str = (f'доброго времени суток 👋, {message.from_user.first_name}!\n'
                            f'Вас приветствует бот который поможет найти нужные вам товары из интернета. 💻')
        file_picture: IO[bytes] = open('./logo.webp', 'rb')
        self.bot.send_photo(message.chat.id, file_picture)
        self.bot.send_message(message.chat.id, text_output)
        self.main_menu(message)

    def main_menu(self, message: telebot.types.Message) -> None:
        """
        Данный метод представляет собой основное меню телеграмм бота. Где пользователю предоставлены основной функционал
        взаимодействия с ним.
        """
        text: str = f'Главное меню 📃'
        marcup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_about = types.KeyboardButton('o боте 🧸')
        button_search = types.KeyboardButton('Поиск товара с сортировкой ⚙️')
        button_only_result = types.KeyboardButton('Найти один результат 🔎')
        button_max_result = types.KeyboardButton('Найти максимум результатов 🔍')
        button_help = types.KeyboardButton('Помощь 💡')
        button_story = types.KeyboardButton('История 📝')
        favorite_button = types.KeyboardButton('Избранное ⭐️')
        marcup.row(button_search)
        marcup.row(button_only_result, button_max_result)
        marcup.row(button_about, button_story)
        marcup.row(button_help, favorite_button)
        self.bot.send_message(message.chat.id, text, reply_markup=marcup)
        self.bot.register_next_step_handler(message, self.main_click_menu)

    def main_click_menu(self, message: telebot.types.Message) -> None:
        """
        Данных метод обрабатывает введенные данные пользователем и перенаправляет в последующий метод задавая
        те или иные параметры в зависимости от выбора пользователя. В Случае отсутствия совпадения пользователь будет
        перенаправлен в основное меню. В случае, если совпадений не будет, пользователю будет выведено сообщение о том
        что команда не была обработана.
        """
        match message.text.lower():
            case command if '/start' in command or 'главное меню' in command or 'main' in command:
                self.main_menu(message)
            case command if 'o боте' in command or '/about' in command:
                self.about_menu(message)
            case command if 'поиск товара с сортировкой' in command or '/custom' in command:
                self.product_search_menu(message)
            case command if 'найти один результат' in command or '/low' in command:
                self.param[message.chat.id] = False
                self.input_search_supplies_menu(message)
            case command if "найти максимум результатов" in command or "/high" in command:
                self.param[message.chat.id] = True
                self.input_search_supplies_menu(message)
            case command if 'помощь' in command or '/help' in command:
                self.helper(message)
            case command if 'история' in command or "/history" in command:
                self.history_menu(message)
            case command if 'избранное' in command or '/favorite' in command:
                self.page[message.chat.id] = 0
                self.create_date_favorite(message)
                self.favorite_menu(message)
            case _:
                self.bot.send_message(message.chat.id, 'Похоже вы ввели что-то ни то.\n '
                                                       'Вам снова доступны команды из главного меню')
                self.main_menu(message)

    def history_menu(self, message: telebot.types.Message) -> None:
        """
        Метод предоставляет пользователю информацию о его последних 10 запросах и выводит их на экран.
        В дальнейшем их можно использовать для повторного вывода.
        Notes:
            Метод обращается к БД. Извлекает данные в виде списка. После чего создаются кнопки через цикл.
            Затем весь список истории будет доступен пользователю для активного использования и обращения к
            временным файлам "./api_site/utils/requests/".
        Raises:
            TypeError: В случае, если в истории пользователя не будет данных, будет вызвано исключение, после чего
            пользователю будет об этом отправлено сообщение.
        """

        try:
            history: List[History] = ManagerDB.read_history(message.from_user.id)
            if len(history) > 0:
                buttons = types.InlineKeyboardMarkup()

                for story in history:  # Обходим список объектов и создаем инлайн-клавиатуру.
                    match story.method:
                        case command if 'down /custom' in command:
                            command = '📉 /custom'
                        case command if 'up /custom' in command:
                            command = '📈 /custom'
                        case command if 'def /custom' in command:
                            command = '📊 /custom'
                        case command if 'one /low' in command:
                            command = '🔎 /low'
                        case command if 'max /high' in command:
                            command = '🔍 /high'

                    button = types.InlineKeyboardButton(''.join(f'{command}: {story.request}'
                                                                f''), callback_data=f'{command} {story.request}')
                    buttons.add(button)
                self.bot.send_message(message.chat.id, 'История...', reply_markup=buttons)
            else:
                raise TypeError(history)
        except TypeError as err:
            logger.info(f"Не удалось обработать запрос в БД от пользователя: @{message.from_user.username} :{err=}")
            self.bot.send_message(message.chat.id, 'Нет данных.')

    def helper(self, message: telebot.types.Message) -> None:
        """
        При обращении к данному методу пользователю будет предоставлен перечень основных команд в боте.
        """
        self.bot.send_message(message.chat.id, self.__text_help)
        marcup_under = types.ReplyKeyboardMarkup(resize_keyboard=True)
        print(type(marcup_under))
        butt = types.KeyboardButton('Главное меню')
        marcup_under.add(butt)
        self.bot.send_message(message.chat.id, 'Для возврата назад, нажмите Главное меню', reply_markup=marcup_under)

    def next_menu_for_custom_request(self, message: telebot.types.Message) -> None:
        """
        Данных метод обрабатывает введенные данные пользователем и перенаправляет в последующий метод задавая
        те или иные параметры в зависимости от выбора пользователя. В Случае отсутствия совпадения пользователь будет
        перенаправлен в основное меню. Об этом не будет выводиться сообщение так как возможен ввод системной команды
        бота.
        """
        self.param[message.chat.id] = None
        match message.text.lower():
            case command if 'составить список без сортировки' in command:
                self.sort[message.chat.id] = None
                self.input_search_supplies_menu(message)
            case command if "составить список по возрастанию цены" in command:
                self.sort[message.chat.id] = False
                self.input_search_supplies_menu(message)
            case command if "составить список по убыванию цены" in command:
                self.sort[message.chat.id] = True
                self.input_search_supplies_menu(message)
            case _:
                self.main_click_menu(message)

    def input_search_supplies_menu(self, message: telebot.types.Message) -> None:
        """
        Данный метод ожидает от пользователя ввод данных для поиска данных, принимает их и передает
        в метод check_text_for_requests_menu().

        Params:
            message: Объект библиотеки PyTeleBotAPI, в котором хранятся данные о сессии и пользователе.

        """

        text_supplies_menu: str = 'Введите название товара: ... 🖍'
        self.bot.send_message(message.chat.id, text_supplies_menu, reply_markup=types.ReplyKeyboardRemove())
        self.bot.register_next_step_handler(message, self.check_text_for_requests_menu)

    def check_text_for_requests_menu(self, message: telebot.types.Message, call_func=None) -> None:
        """
        Данный метод определяет с какими параметрами будет предоставляться пользователю результат

         Params:
            message: Объект библиотеки PyTeleBotAPI, в котором хранятся данные о сессии и пользователе.
            param: bool: С помощью данного параметра определяется какой вывод данных необходимо совершить.
            sort: bool: С помощью данного параметра определяется тип сортировки данных.


        Notes:
            После того как пользователь ввел текст запроса, будет произведена проверка.
            Где будет проверен тип данных, после чего длинна текста, а затем об отсутствии содержания
            в запросе исключительно цифр и будет произведена проверка на содержание символа "/" в начале строки.
            В случае истины, данное сообщение будет расценено как попытка ввести основную команду бота,
            после чего данное сообщение будет обработано методом main_click_menu(). Иначе Пользователю будет выведено
            сообщение о том что был не корректный ввод данных.
            Пройдя проверку данных создается словарь с параметрами пользователя и его запроса, которые передаются
            в базу данных. И Пользователю выводится сообщение о том что начался поиск.
            Проверяются параметры поиска, где в случае отсутствия параметра будет создано обращение к API.
            После получения результат будут проверены параметры сортировки данных. И затем данные будут переданы в
            дальнейший метод result_price_menu().
            В случае если параметр не None, производятся дополнительные операции, такие как предоставление одного
            результата в случае False. Или предоставление всех результатов в случае True. Затем так же результат
            будет передан в следующий метод result_price_menu().

        Raises:
            TypeError: Возникает, в случае если сервер не ответил, или возникли проблемы с формированием
            результата ответа. Так как результатом может являться пустой список.
            В результате чего об этом будет сделана соответствующая запись в лог файле.
            После чего пользователь будет перенаправлен в меню ввода запроса повторно.

        """
        if call_func is None:  # Если пользователь обращается к истории запросов, то будет передан параметр поиска.
            text_input_user: str = message.text
        else:
            text_input_user: str = call_func

        text_search: str = 'Поиск...'
        sort = self.sort.get(message.chat.id)  # Запрашиваем параметры поиска.
        param = self.param.get(message.chat.id)
        try:
            if isinstance(text_input_user, str):  # Проверка корректных данных и наличие исполнительных команд.
                if (len(text_input_user) > 30 and not all(True for i in text_input_user if i.isdigit())
                        or (text_input_user.startswith('/'))):

                    if text_input_user.startswith('/'):
                        self.main_click_menu(message)
                    else:
                        self.bot.send_message(message.chat.id, 'Запрос не корректен.\n'
                                                               'Возможно текст слишком большой или данные не корректны')
                        self.input_search_supplies_menu(message)
                else:
                    if call_func is None:  # Не обновляем историю. Повторный запрос.
                        ManagerDB.write_db_story(id_user=message.from_user.id,
                                                 message=message, param=param, sort=sort)
                    self.bot.send_message(message.chat.id, text_search)
                    # Создаем кэш для того что бы не дублировать добавленные элементы.
                    self.create_date_favorite(message)
                    self.page[message.chat.id] = 0  # Сбрасываем страницу

                    if param is None:  # Вывод с сортировкой.
                        result: List[Product] = get_api(method='Поиск товара', product=text_input_user, country='ru',
                                                        language='ru',
                                                        page=2)
                        if sort is True:  # Вывод отсортированного результата по убыванию.
                            self.sort[message.chat.id] = None
                            result = sorted(result, key=lambda x: x.get_price(), reverse=True)

                        elif sort is False:  # Вывод отсортированного результата по увеличению.
                            self.sort[message.chat.id] = None
                            result = sorted(result, key=lambda x: x.get_price(), reverse=False)

                        if len(result) > 15:
                            self.data[message.chat.id] = result[:15]

                        else:
                            self.data[message.chat.id] = result
                        self.result_price_menu(message)

                    elif param is False:  # Выдаем один результат
                        self.param[message.chat.id] = None
                        result: List[Product] = [random.choice(
                            get_api(method='Поиск товара', product=text_input_user, country='ru', language='ru',
                                    page=1))]
                        self.data[message.chat.id] = result
                        self.result_price_menu(message)

                    else:  # Выдаем максимальное кол-во результатов=30, можно расшить до page += 1.
                        result: List[Product] = get_api(method='Поиск товара', product=text_input_user, country='ru',
                                                        language='ru',
                                                        page=3)
                        self.data[message.chat.id] = result
                        self.param[message.chat.id] = None
                        self.result_price_menu(message)
            else:
                raise TypeError('Не верный тип данных.')

        except TypeError as err:
            logger.error(
                f'tg_bot/tg_bot_util.py Не удалось обработать запрос от пользователя @{message.from_user.username}'
                f', запрос {message.text}, param = {param}, sort = {sort}.  TypeError: {err}', )
            self.bot.send_message(message.chat.id, 'Произошла ошибка. попробуйте еще раз.')
            self.main_click_menu(message)

    def result_price_menu(self, message: telebot.types.Message, previous_message=None,
                          favorite_add: Optional[bool] = False, favorite_del: Optional[bool] = False) -> None:
        """
        Метод предоставляет запрашиваемую информацию в виде изображения товара, его названия,
        описания, характеристик, доставки, рейтинга и цены.

        Params:
            message: Объект библиотеки PyTeleBotAPI, в котором хранятся данные о сессии и пользователе.
            product: List[Product] : Объект содержащий информацию о товаре.
            previous_message: (boll): Параметр отвечает за удаление старых сообщений.
            favorite_add: Optional[bool]: Параметр отвечает за добавление в Избранное.
            favorite_del: Optional[bool]: Параметр отвечает за удаление из Избранного.


        Notes:
            Является основным методом, который предоставляет интерфейс с результатам запроса
            непосредственно пользователю. На первом этапе проходит проверка формата ответа. В случае, если будет иной
            тип данных, будет вызвано исключение TypeError. Иначе в список объектов с результатами будет передан
            индекс (page_num) и на его основании будет сформирован результат для вывода информации пользователю
            на экран. Затем будет отправлено изображение и закрепленное текстовое сообщение с описанием
            того что, что было на изображении, а так же будет отправлена ссылка на ресурс,
            где можно будет подробнее ознакомиться с товаром.
            При навигации в меню с результатами ситуативно формируется навигационное меню.
            Пользователю всегда будет доступно Основное меню: меню возврата в главное окно,
            ссылка и Избранное. В случае, если список предоставленных ответов будет равен единице, то будет выводиться
            Основное меню. В ином случае будет производиться проверка, если индекс больше нуля,
            но меньше длины списка -2, то будут доступны навигационные кнопки вперед и назад.
            В случае если индекс равен длин списка -1, то будет доступно назад.
            А так же, при начале просмотра доступно только вперед.

        Raises:
             TypeError: Возникает, в случае если сервер не ответил, или возникли проблемы с формированием
             результата ответа. Так как результатом может являться пустой список.
             В результате чего об этом будет сделана соответствующая запись в лог файле.
             После чего пользователь будет перенаправлен в меню ввода запроса повторно.

        """
        page_num: int = self.page.get(message.chat.id, 0)  # Собираем данные.
        result: list = self.data.get(message.chat.id, None)
        sort: bool = self.sort.get(message.chat.id)
        param: bool = self.param.get(message.chat.id)
        cache_list: List = self.favorite_dict_cache.get(message.chat.id)
        try:
            if isinstance(result, list) and len(result) >= 1:  # Структурируем данные.
                text: str = f'Для навигации используйте клавиатуру ⬅️[{page_num + 1}-й из {len(result)}]➡️.'
                any_product: Product = result[page_num]
                pattern: str = read_pattern(any_product)
                url: str = any_product.get_offer_page_url()
                pict: bytes = self.cache_foto.check_cache(pattern=pattern, link=any_product.get_link_photo())
                # Создаем клавиатуру.
                marcup_inline = types.InlineKeyboardMarkup()
                marcup_inline.add(types.InlineKeyboardButton('Ссылка для перехода 🔗', url=url))
                button_next = types.InlineKeyboardButton('следующий ➡', callback_data='next')
                button_back = types.InlineKeyboardButton('⬅ предыдущий', callback_data='back')
                button_main = types.InlineKeyboardButton('Главное меню 📃', callback_data='main')

                if favorite_add:  # Добавляем в избранное и создаем соответсвующую кнопку
                    cache_list.append(url)
                    self.favorite_dict_cache[message.chat.id] = cache_list
                    ManagerDB.write_favorite(id_user=message.chat.id, link_photo=any_product.get_link_photo(),
                                             about=pattern, link_web=url)
                    marker = '🗑'
                    button_favorite = types.InlineKeyboardButton(f'Удалить из избранного '
                                                                 f'{marker}', callback_data='favorite_del')

                    marcup_inline.add(button_favorite)

                elif favorite_del:  # Удаляем из избранного и создаем соответсвующую кнопку
                    cache_list.pop(cache_list.index(url))
                    ManagerDB.del_favorite(id_user=message.chat.id, link=url)
                    marker = '⭐️'
                    button_favorite = types.InlineKeyboardButton(f'Добавить в избранное'
                                                                 f' {marker}', callback_data='favorite')
                    marcup_inline.add(button_favorite)

                else:
                    #  Проверяем кеш и создаем кнопки "Добавить/Удалить".
                    if len(self.favorite_dict) > 0 and url in cache_list:
                        marker = '🗑'
                        button_favorite = types.InlineKeyboardButton(f'Удалить из избранного '
                                                                     f'{marker}', callback_data='favorite_del')
                        marcup_inline.add(button_favorite)

                    else:
                        marker = '⭐️'
                        button_favorite = types.InlineKeyboardButton(f'Добавить в избранное '
                                                                     f'{marker}', callback_data='favorite')
                        marcup_inline.add(button_favorite)

                if len(result) != 1:  # Создаем кнопки навигации.
                    if (page_num > 0) and (page_num <= len(result) - 2):
                        marcup_inline.add(button_back, button_next)
                    elif page_num == len(result) - 1:
                        marcup_inline.add(button_back)
                    else:
                        marcup_inline.add(button_next)

                marcup_inline.add(button_main)  # Все готово к отправке сообщения.
                self.bot.send_photo(message.chat.id, pict, caption=f'{pattern}\n{text}', reply_markup=marcup_inline)

                if previous_message is not None:  # Проверяем старое сообщение.
                    try:
                        self.bot.delete_message(message.chat.id, previous_message.id)
                    except telebot.apihelper.ApiException as er:
                        logger.debug("Ошибка удаления сообщения.", er)
            else:
                raise TypeError("Тип данных запроса некорректен")

        except TypeError as err:  # Обрабатываем ошибки не удачного запроса и передаем его параметры.
            logger.error(
                f'tg_bot/tg_bot_util.py Не удалось обработать запрос от пользователя @{message.from_user.username}'
                f' результат запроса: {result}, запрос {message.text}, param = {param}, sort = {sort}.'
                f' TypeError: {err}', )
            self.bot.send_message(message.chat.id, 'Произошла ошибка. попробуйте еще раз.')
            self.input_search_supplies_menu(message)

    def product_search_menu(self, message: telebot.types.Message) -> None:
        """
        Метод предоставляет пользователю /custom меню предоставления результатов.
        """
        text: str = 'Прежде чем начать, выберите в каком порядке хотите видеть товары:'
        self.bot.send_message(message.chat.id, text)
        marcup_under = types.ReplyKeyboardMarkup(resize_keyboard=True)
        butt = types.KeyboardButton('Главное меню 📃')
        price_butt = types.KeyboardButton("Составить список без сортировки 📊")
        min_price_butt = types.KeyboardButton("Составить список по возрастанию цены 📈")
        max_price_butt = types.KeyboardButton("Составить список по убыванию цены 📉")
        marcup_under.add(butt)
        marcup_under.add(price_butt)
        marcup_under.add(max_price_butt)
        marcup_under.add(min_price_butt)
        self.bot.send_message(message.chat.id, 'Для возврата назад, нажмите Главное меню 📃', reply_markup=marcup_under)
        self.bot.register_next_step_handler(message, self.next_menu_for_custom_request)

    def create_date_favorite(self, message: telebot.types.Message) -> None:
        """
        Метод обращается к одноименной функции модуля ./bot_utils/bot_data. Которая обрабатывает данные пользователя.

        Params:
            message: Объект PyTeleBotAPI.

        Returns:
            None

        Notes:
            Метод предоставляет данные пользователя о сохраненных в БД избранных товаров. Но этос основании формируется
            словарь где ключом является id пользователя, а данными являются список товаров. Так же формируется еще один
            словарь с подобным ключом, но в списке хранятся только url ссылки. Это нужно для того, что бы при
            обращении пользователя к новому писку или к истерии, были отображены товары, которые ранее были уже
            добавлены в список Избранных. Что в конечном итоге поможет исключить дублирование информации и
            пользователю будет легче ориентироваться среди новой информации.
        """

        create_data = create_date_favorite(id_user=message.chat.id, favorite_dict=self.favorite_dict,
                                           favorite_dict_cache=self.favorite_dict_cache)
        self.favorite_dict, self.favorite_dict_cache = create_data

    def favorite_menu(self, message: telebot.types.Message, previous_message=None,
                      del_fav: Optional[bool] = False) -> None:
        """
        Метод предоставляем доступ к сохраненным данным и выводит их на экран пользователя.
        Params:
            del_fav: Отвечает за удаление из списка сохраненных файлов.
            previous_message: Отвечает за удаление сообщения.
        Returns:
            None
        Notes:
            Метод обрабатывает список Избранных товаров, где в хоте его работы, будет формироваться интерфейс
            клавиатуры в зависимости от полученных данных. Пользователю всегда будет доступна ссылка на страницу товара
            и главное меню. Так же в зависимости от длины списка будут предоставлена клавиатура перехода к следующему
            и предыдущему товару. Пока товар находится в списке избранного, отображается клавиатура удаления из данного
            списка. После чего данная опция не будет отображаться под этим товаром из списка конкретного пользователя.
        Raises:
            TypeError: Исключение будет вызвано в случае отсутствия данных в БД о данном пользователе.
            После чего пользователю будет выведено соответствующее сообщение.
        """

        page_num: int = self.page.get(message.chat.id, 0)  # Собираем данные.
        favorite_data: List = self.favorite_dict.get(message.chat.id, [])
        list_cache: List = self.favorite_dict_cache.get(message.chat.id)
        try:
            if isinstance(favorite_data, list) and len(favorite_data) > 0:
                any_product: list = favorite_data[page_num]  # Извлекаем данные.
                url: str = any_product[0]
                marcup_inline = types.InlineKeyboardMarkup()  # Формируем образ клавиатуры.

                if del_fav:  # Удаляем элемент из БД.
                    list_cache.pop(list_cache.index(url))
                    any_product: list = favorite_data[page_num]
                    url: str = any_product[0]
                    marcup_inline.add(types.InlineKeyboardButton('Ссылка для перехода 🔗', url=url))
                    ManagerDB.del_favorite(id_user=message.chat.id, link=url)
                    self.create_date_favorite(message)
                else:
                    if url in list_cache:
                        del_fav_butt = types.InlineKeyboardButton('Удалить из избранного 🗑', callback_data="del_fav")
                        marcup_inline.add(del_fav_butt)
                    marcup_inline.add(types.InlineKeyboardButton('Ссылка для перехода 🔗', url=url))
                button_next = types.InlineKeyboardButton('следующий ➡', callback_data='next_favor')
                button_back = types.InlineKeyboardButton('⬅ предыдущий', callback_data='back_favor')
                button_main = types.InlineKeyboardButton('Главное меню 📃', callback_data='main')
                pict: bytes = self.cache_foto.check_cache(pattern=any_product[2], link=any_product[1])

                if len(favorite_data) != 1:
                    if (page_num > 0) and (page_num <= len(favorite_data) - 2):
                        marcup_inline.add(button_back, button_next)
                    elif page_num >= len(favorite_data) - 1:
                        marcup_inline.add(button_back)
                    else:
                        marcup_inline.add(button_next)
                text: str = f'Для навигации используйте клавиатуру ⬅️[{page_num + 1}-й из {len(favorite_data)}]➡️'
                marcup_inline.add(button_main)  # Данные и клавиатура отформатированы и готовы к отправке пользователю.
                self.bot.send_photo(message.chat.id, pict, caption=f'{any_product[2]}\n{text}',
                                    reply_markup=marcup_inline)

                if previous_message is not None:  # Удаляем старое сообщение.
                    try:
                        self.bot.delete_message(message.chat.id, previous_message.id)
                    except telebot.apihelper.ApiException as er:
                        logger.debug("Ошибка удаления сообщения.", er)

            else:
                raise TypeError("Запрос БД не дал результатов")

        except TypeError as err:  # В случае отсутствия данных о пользователе, будет вызвано исключение.
            logger.info(
                f"Не удалось обработать запрос в БД от пользователя: @{message.from_user.username} :{err=}")
            # Пользователь получает информацию об отсутствии данных.
            self.bot.send_message(message.chat.id, 'Нет данных.')

    def about_menu(self, message) -> None:
        """
        Метод предоставляет пользователю развернутую информацию о возможностях бота.
        Notes:
            Пользователь получает ответ от бота с подробным описаем, от куда непосредственно имеет доступ
             к их применению используя команды. Команды доступны в любом разделе бота, что упрощает отмену каких-либо
             действий, примеру таких как ввод данных непосредственно в меню ввода текста. Или в любых других местах,
             где может отсутствовать клавиатура.
        """
        self.bot.send_message(message.chat.id, self.__about_text)
        marcup_under = types.ReplyKeyboardMarkup(resize_keyboard=True)
        butt = types.KeyboardButton('Главное меню 📃')
        marcup_under.add(butt)
        self.bot.send_message(message.chat.id, 'Для возврата назад, нажмите Главное меню 📃', reply_markup=marcup_under)
        self.bot.register_next_step_handler(message, self.main_click_menu)

    def run(self) -> None:
        """
        Метод выполняет функцию запуска бота.
        """

        @self.bot.message_handler(commands=["start"])
        def start(message) -> None:
            """
            Метод запускает сеанс с пользователем.
            """
            self.start_menu(message)

        @self.bot.message_handler(commands=["help"])
        def main_helper(message) -> None:
            """
            Метод предоставляет доступ к командам бота.
            """
            self.helper(message)

        @self.bot.message_handler(commands=['history'])
        def main_history(message) -> None:
            """
            Метод предоставляет доступ к истории запросов пользователя.
            """
            self.history_menu(message)

        @self.bot.message_handler(commands=['low'])
        def main_low(message) -> None:
            """
            Метод предоставляет доступ к меню ввода запроса с минимальными результатами.
            """
            self.param[message.chat.id] = False
            self.sort[message.chat.id] = None
            self.input_search_supplies_menu(message)

        @self.bot.message_handler(commands=['high'])
        def main_high(message) -> None:
            """
            Метод предоставляет доступ к меню ввода запроса с максимальными результатами.
            """
            self.param[message.chat.id] = True
            self.sort[message.chat.id] = None
            self.input_search_supplies_menu(message)

        @self.bot.message_handler(commands=['custom'])
        def main_custom(message) -> None:
            """
            Метод предоставляет доступ к кастомному меню.
            """
            self.param[message.chat.id] = None
            self.sort[message.chat.id] = None
            self.product_search_menu(message)

        @self.bot.callback_query_handler(func=lambda callback_query: True)
        def callback(callback_query) -> None:
            """
            Данная функция отлавливает Инлайн команды, после чего происходит определение
             данной команды и дальнейшее ее исполнение.
            Args:
                callback_query: данный объект содержит результат использования InlineKeyboardMarkup()
            Returns:
                None
            Notes:
                В Первую очередь проверяются простые команды.
                Если он не будут определены, будут проверяться команды обращения в историю событий.
            """

            if 'next_favor' in callback_query.data:
                self.page[callback_query.from_user.id] += 1
                self.favorite_menu(callback_query.message, previous_message=callback_query.message)

            elif 'back_favor' in callback_query.data:
                self.page[callback_query.from_user.id] -= 1
                self.favorite_menu(callback_query.message, previous_message=callback_query.message)

            elif "del_fav" in callback_query.data:
                self.favorite_menu(callback_query.message, previous_message=callback_query.message, del_fav=True)

            elif 'next' in callback_query.data:
                self.page[callback_query.from_user.id] += 1
                self.result_price_menu(callback_query.message, previous_message=callback_query.message,
                                       favorite_add=False)

            elif 'back' in callback_query.data:
                self.page[callback_query.from_user.id] -= 1
                self.result_price_menu(callback_query.message, previous_message=callback_query.message,
                                       favorite_add=False)

            elif "favorite_del" in callback_query.data:
                self.result_price_menu(callback_query.message, previous_message=callback_query.message,
                                       favorite_del=True)

            elif 'favorite' in callback_query.data:
                self.result_price_menu(callback_query.message, previous_message=callback_query.message,
                                       favorite_add=True)

            elif 'main' in callback_query.data:
                self.page[callback_query.from_user.id] = 0
                self.main_menu(callback_query.message)

            elif '/' in callback_query.data:
                self.page[callback_query.from_user.id] = 0

                if len(callback_query.data.split()) > 1:
                    rq: str = "".join(f'{text} ' for text in callback_query.data.split()[2:])[:-1]  # создаем запрос

                    if '/custom' in callback_query.data:
                        self.param[callback_query.from_user.id] = None

                        if '📈' in callback_query.data:
                            self.sort[callback_query.from_user.id] = True

                        elif "📉" in callback_query.data:
                            self.sort[callback_query.from_user.id] = False

                        elif '📊' in callback_query.data:
                            self.sort[callback_query.from_user.id] = None
                        self.check_text_for_requests_menu(callback_query.message, call_func=rq)

                    elif "/high" in callback_query.data and len(callback_query.data) > len('/high'):
                        self.param[callback_query.from_user.id] = True
                        self.check_text_for_requests_menu(callback_query.message, call_func=rq)
                    elif '/low' in callback_query.data and len(callback_query.data) > len('/low'):
                        self.param[callback_query.from_user.id] = False
                        self.check_text_for_requests_menu(callback_query.message, call_func=rq)

        @self.bot.message_handler()
        def remain(message) -> None:
            """
            Метод отлавливает все-то что не относится к основным командам.
            """
            self.main_click_menu(message)
