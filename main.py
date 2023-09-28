from tg_bot import Bot
from common_utils import check_status_cache_of_files

if __name__ == '__main__':
    check_status_cache_of_files()
    bot = Bot()
    bot.run()  # данных модуль инициализирует запуск бота.
    bot.bot.polling(none_stop=True)
