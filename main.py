from aiogram.utils import executor #Модуль для запуска бота
from loader import dp, bot
from loader import on_startup

from handlers import start
from handlers import check


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)