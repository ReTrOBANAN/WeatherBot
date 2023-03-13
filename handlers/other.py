from loader import dp, bot
from aiogram import Bot, types

@dp.message_handler(commands=['start', 'help']) # Ответ на команду /start
async def start(msg: types.Message):
    mess = f'Привет, <b>{msg.from_user.first_name}</b>!\n' \
           f'<u>Вот что я могу:</u>\n' \
           f'1) Напишите команду «/now Ваш город»\n' \
           f'2) Напишите команду «/tom Ваш город»\n' \
           f'Все данные взяты с Google и Openweathermap'
    await bot.send_message(msg.from_user.id, mess, parse_mode='html')

