from loader import bot, dp
from aiogram import Bot, types, Dispatcher
import requests # Модуль для обработки URL
from bs4 import BeautifulSoup # Модуль для работы с HTML
from loader import token

@dp.message_handler(content_types=['text'])  # Забрать команду пользователя
async def check(msg: types.Message):
    city_spisok = []
    get_message_bot = msg.text.strip().lower().split(' ')
    if get_message_bot[0] == '/now':  # Команда /now
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/find",  # Парсинг Id города
                               params={'q': get_message_bot[1], 'type': 'like', 'units': 'metric', 'APPID': token})
            data = res.json()
            cities = ["{} ({})".format(d['name'], d['sys']['country'])
                      for d in data['list']]
            city_id = data['list'][0]['id']
        except Exception as e:
            await bot.send_message(msg.from_user.id, '<b>Введите корректный город</b>', parse_mode='html')

        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/weather",  # Парсинг погоды на сегодня
                               params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': token})
            weather_req = requests.get(f'https://api.openweathermap.org/data/2.5/weather&appid={token}'.format(token))
            data = res.json()
            cur_temp = '{0:+3.0f}'.format(data['main']['temp'])
            cur_feels = '{0:+3.0f}'.format(data['main']['feels_like'])
            cur_humid = data['main']['humidity']
            cur_press = data['main']['pressure']
            cur_wind = data['wind']['speed']
            clouds = data['clouds']
            cur_clouds = clouds['all']
            cur_weather = data['weather'][0]['description']
        except Exception as ex:
            pass
        try:
            emoji = ''
            url_now = f'https://www.google.com/search?q={get_message_bot[1]}+weather+now&oq=ново&aqs=chrome.0.69i59j69i57j69i59l2j0i131i433i512j69i61l3.793j1j7&sourceid=chrome&ie=UTF-8'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
            full_page = requests.get(url_now, headers=headers)
            soup = BeautifulSoup(full_page.content, 'html.parser')
            city = soup.findAll('div', {'class': 'wob_loc', 'class': 'q8U8x', 'id': 'wob_loc'})
            city_now = city[0].text.split(',')
            weather_now = soup.findAll("span", {'id': "wob_dc"})
            temp_now = soup.findAll("span", {"class": "wob_t", "class": "q8U8x", 'id': "wob_tm"})
            temp_now_far = soup.findAll("span", {"class": "wob_t", 'id': "wob_ttm"})
            now_vlajnost = soup.findAll("span", {'id': 'wob_hm'})
            now_osadki = soup.findAll("span", {'id': 'wob_pp'})
            now_veter = soup.findAll("span", {"class": "wob_t", 'id': 'wob_ws'})
            if cur_weather == 'ясно':
                emoji = '☀️'
            elif cur_weather == 'переменная облачность':
                emoji = '⛅'
            elif cur_weather == 'небольшая облачность':
                emoji = '🌤'
            elif cur_weather == 'облачно с прояснениями':
                emoji = '⛅'
            elif cur_weather == 'пасмурно':
                emoji = '☁️'
            elif cur_weather == 'небольшой дождь':
                emoji = '🌧'
            elif cur_weather == 'дождь':
                emoji = '🌧'
            elif cur_weather == 'облачно':
                emoji = '☁️'
            elif cur_weather == 'снег':
                emoji = '🌨️'
            elif cur_weather == 'небольшой снег':
                emoji = '🌨️'
            elif cur_weather == 'гроза':
                emoji = '⛈'
            elif cur_weather == 'туман':
                emoji = '🌫'
            elif cur_weather == 'небольшой снегопад':
                emoji = '🌨️'
            elif cur_weather == 'местами ливни':
                emoji='⛈️'
            elif cur_weather == 'ливни':
                emoji = '⛈️'
            #####################
            final_mess = f'<b><u>Сейчас</u></b>\n' \
                         f'В городе {get_message_bot[1].title()} сейчас {cur_weather} {emoji}\n' \
                         f'Температура около {cur_temp}°\n' \
                         f'Ощущается как {cur_feels}°\n' \
                         f'Давление: {cur_press} мм рт. ст\n' \
                         f'Облачность: {cur_clouds}%\n' \
                         f'Влажность: {now_vlajnost[0].text}\n' \
                         f'Вероятность осадков: {now_osadki[0].text}\n' \
                         f'Ветер {cur_wind} м/с'
            await bot.send_message(msg.from_user.id, final_mess, parse_mode='html')
        except Exception as ex:
            pass
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                               params={'id': city_id, 'units': 'metric', 'cnt' : '16','lang': 'ru', 'APPID': token})
            data = res.json()
            for i in data['list']:
                message = i['dt_txt'], '{0:+3.0f}'.format(i['main']['temp']), i['weather'][0]['description']
                hour_day = i['dt_txt']
                hour_temp = '{0:+3.0f}'.format(i['main']['temp'])
                hour_weather = i['weather'][0]['description']
                hour_wind = i['wind']['speed']
                hour_day = hour_day.split('-')
                hourday = hour_day[2].split(' ')
                if hour_day[1] == '01':
                    month = 'янв'
                if hour_day[1] == '02':
                    month = 'фев'
                if hour_day[1] == '03':
                    month = 'мар'
                if hour_day[1] == '04':
                    month = 'апр'
                if hour_day[1] == '05':
                    month = 'май'
                if hour_day[1] == '06':
                    month = 'июня'
                if hour_day[1] == '07':
                    month = 'июля'
                if hour_day[1] == '08':
                    month = 'авг'
                if hour_day[1] == '09':
                    month = 'сен'
                if hour_day[1] == '10':
                    month = 'окт'
                if hour_day[1] == '11':
                    month = 'ноя'
                if hour_day[1] == '12':
                    month = 'дек'
                if hour_weather == 'ясно':
                    hour_emoji = '☀️'
                elif hour_weather == 'переменная облачность':
                    hour_emoji = '⛅'
                elif hour_weather == 'небольшая облачность':
                    hour_emoji = '🌤'
                elif hour_weather == 'облачно с прояснениями':
                    hour_emoji = '⛅'
                elif hour_weather == 'пасмурно':
                    hour_emoji = '☁️'
                elif hour_weather == 'небольшой дождь':
                    hour_emoji = '🌧'
                elif hour_weather == 'дождь':
                    hour_emoji = '🌧'
                elif hour_weather == 'облачно':
                    hour_emoji = '☁️'
                elif hour_weather == 'снег':
                    hour_emoji = '🌨️'
                elif hour_weather == 'небольшой снег':
                    hour_emoji = '🌨️'
                elif hour_weather == 'гроза':
                    hour_emoji = '⛈'
                elif hour_weather == 'туман':
                    hour_emoji = '🌫'
                elif hour_weather == 'местами ливни':
                    hour_emoji = '⛈️'
                elif hour_weather== 'небольшой снег':
                    hour_emoji = '🌨️'
                hour_mess = f'{hourday[0]} {month}, {hourday[1]}' \
                            f' {hour_temp}°' \
                            f' {hour_wind} м/c' \
                            f' {hour_weather} {hour_emoji}\n'
                city_spisok.append(hour_mess)
            hour_mess = f'{city_spisok[0]}\n{city_spisok[1]}\n{city_spisok[2]}\n{city_spisok[3]}\n{city_spisok[4]}\n{city_spisok[5]}\n{city_spisok[6]}\n{city_spisok[7]}\n{city_spisok[8]}\n{city_spisok[9]}\n{city_spisok[10]}\n{city_spisok[11]}\n{city_spisok[12]}\n{city_spisok[13]}\n{city_spisok[14]}\n{city_spisok[15]}'
            await bot.send_message(msg.from_user.id, hour_mess, parse_mode='html')
        except Exception as ex:
            print(ex)

    elif get_message_bot[0] == '/tom':  # Ответ на команду /tom\
        try:
            url_tomorrow = f'https://www.google.com/search?q={get_message_bot[1]}+weather+tomorrow&oq=moscow+weather+to&aqs=chrome.1.69i57j0i512l2j0i22i30j0i10i22i30j0i22i30l5.9477j0j7&sourceid=chrome&ie=UTF-8'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
            full_page = requests.get(url_tomorrow, headers=headers)  # Парсинг погоды на завтра
            soup = BeautifulSoup(full_page.content, 'html.parser')
            city = soup.findAll('div', {'class': 'wob_loc', 'class': 'q8U8x', 'id': 'wob_loc'})
            city = city[0].text.split(',')
            weather_tom = soup.findAll("span", {'id': "wob_dc"})
            temp_tom = soup.findAll("span", {"class": "wob_t", "class": "q8U8x", 'id': "wob_tm"})
            temp_tom_far = soup.findAll("span", {"class": "wob_t", 'id': "wob_ttm"})
            vlajnost_tom = soup.findAll("span", {'id': 'wob_hm'})
            osadki_tom = soup.findAll("span", {"id": "wob_pp"})
            veter_tom = soup.findAll("span", {"class": "wob_t", 'id': 'wob_ws'})
            if weather_tom[0].text.strip().lower() == 'ясно':
                emoji = '☀️'
            elif weather_tom[0].text.strip().lower() == 'переменная облачность':
                emoji = '⛅'
            elif weather_tom[0].text.strip().lower() == 'небольшая облачность':
                emoji = '🌤'
            elif weather_tom[0].text.strip().lower() == 'облачно с прояснениями':
                emoji = '⛅'
            elif weather_tom[0].text.strip().lower() == 'пасмурно':
                emoji = '☁️'
            elif weather_tom[0].text.strip().lower() == 'небольшой дождь':
                emoji = '🌧'
            elif weather_tom[0].text.strip().lower() == 'дождь':
                emoji = '🌧'
            elif weather_tom[0].text.strip().lower() == 'облачно':
                emoji = '☁️'
            elif weather_tom[0].text.strip().lower() == 'снег':
                emoji = '🌨️'
            elif weather_tom[0].text.strip().lower() == 'небольшой снег':
                emoji = '🌨️'
            elif weather_tom[0].text.strip().lower() == 'гроза':
                emoji = '⛈'
            elif weather_tom[0].text.strip().lower() == 'туман':
                emoji = '🌫'
            elif weather_tom[0].text.strip().lower() == 'небольшой снегопад':
                emoji = '🌨️'
            elif weather_tom[0].text.strip().lower() == 'местами ливни':
                emoji = '⛈️'
            elif weather_tom[0].text.strip().lower() == 'cнегопад':
                emoji = '🌨️'
            else:
                emoji = ''
            final_mess = f'<b><u>Завтра</u></b>\n' \
                         f'В городе {city[0]} завтра {weather_tom[0].text.strip().lower()} {emoji}\n' \
                         f'Температура около {temp_tom[0].text}°\n' \
                         f'Влажность: {vlajnost_tom[0].text}\n' \
                         f'Вероятность осадков: {osadki_tom[0].text}\n' \
                         f'Ветер {veter_tom[0].text}'

            await bot.send_message(msg.from_user.id, final_mess, parse_mode='html')

        except Exception as ex:
            await bot.send_message(msg.from_user.id, '<b>Введите корректный город</b>', parse_mode='html')
    else:
        await bot.send_message(msg.from_user.id, '<b>Я неправильно вас понял</b>', parse_mode='html')
