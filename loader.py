from aiogram.dispatcher import Dispatcher
from aiogram import Bot, types

TOKEN = '5763619550:AAHoBm6boCMUvnw4UNamG-u_3d7ymYj183M'
token = 'e5be69a83523d76ccec6de8af518f8e9'
# создание бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def on_startup(_):
    print('Bot on start')
