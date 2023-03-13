from aiogram.dispatcher import Dispatcher
from aiogram import Bot, types

TOKEN = 'YourTelegramBotToken'
token = 'YourOpenWeatherMapToken'
# создание бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def on_startup(_):
    print('Bot on start')
