  
import mysql.connector
import nest_asyncio
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import  InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from config import o_weather_token, config_data
from datetime import datetime

nest_asyncio.apply()

bot = Bot(token='WRITE_HERE_YOUR_BOT_TOKEN')
dp = Dispatcher(bot)

weather_keyboard = types.InlineKeyboardMarkup(row_width=1)
weather_bt = InlineKeyboardButton('Weather in Mocsow 🌡', callback_data='button1')
help_bt = InlineKeyboardButton('Touch me to know more', callback_data='button2')
weather_keyboard.add(weather_bt)
weather_keyboard.add(help_bt)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Wow! Hey there! \nPlease write me your phone number in format "+7__________", so I will identify you :)')
    

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def phone_checker(message: types.Message):
    telegram_id = message.from_user.id
    
    cnx = mysql.connector.connect(**config_data)
    cursor = cnx.cursor()
    checking = cursor.execute(f"SELECT user_name FROM telebot WHERE telegram_id={telegram_id}")
    print(checking)
    telegram_id_checker = cursor.fetchone()
    cursor.close()

    if telegram_id_checker is None:
        telegram_user_phone = message.text
        cursor = cnx.cursor()
        data_up = cursor.execute(f"UPDATE telebot SET telegram_id = {telegram_id} WHERE user_phone_number='{telegram_user_phone}'")
        cnx.commit()
        cursor.close()
        cnx.close()

        cnx = mysql.connector.connect(**config_data)
        cursor = cnx.cursor()
        cursor.execute(f"SELECT user_name FROM telebot WHERE user_phone_number='{telegram_user_phone}'")
        name = cursor.fetchone()[-1]
        cursor.close()
        print('1')
        await message.answer(f'Wow! Hey there! \nHow is it going, {name}? So let me introduce myself! \n\
Press "Touch me to know more" button!',\
            reply_markup=weather_keyboard)

    else:
        cursor = cnx.cursor()
        cursor.execute(f"SELECT user_name FROM telebot WHERE telegram_id={telegram_id}")
        name = cursor.fetchone()[-1]
        cursor.close()
        await message.answer(f'Wass up, {name}! \nHow is your week? Hope, well!\n\
Guess, I know what you want! TOUCH MY WEATHER BUTTON! NOW!',\
        reply_markup=weather_keyboard)
    cnx.close()


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer('Hello! My name is Weatherin and I will help you to recognize what is going on behind the window!\n\nIf you want to know the weather just write me anytime and anything (even "kalyabalyaki" is okay!)',\
         reply_markup=weather_keyboard)

         
@dp.callback_query_handler(lambda c: c.data == "button2")
async def help_bt_func(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Hello! My name is Weatherin and I will help you to recognize what is going on behind the window!\n\n\
If you want to know the weather just write me anytime and anything (even "kalyabalyaki" is okay!) ')
         

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def lil_info(message: types.Message):
    await message.answer('If you want to know the weather, please push the button',\
         reply_markup=weather_keyboard)


@dp.callback_query_handler(lambda c: c.data == "button1")
async def weather(callback_query: types.CallbackQuery):
    dict_of_wead_emo = {
        'Clear': '\U00002600 clear ',
        'Clouds': '\U00002601 clouds',
        'Mist': '\U00001F32B mist ',
        'Fog': '\U00001F32B mist',
        'Rain': '\U00001F327 rain',
        'Drizzle': '\U00002614 drizzle',
        'Snow': '\U00001F328 snow',
        'Thunderstorm': '\U00001F329 thunderstorm'}

    req = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q=Moscow&appid={o_weather_token}&units=metric')
    data = req.json()

    temp_current = data['main']['temp']
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    feels_like = data['main']['feels_like']
    wind_speed = data['wind']['speed']
    sunrise_t = datetime.fromtimestamp(data['sys']['sunrise'])
    sunset_t = datetime.fromtimestamp(data['sys']['sunset'])
    total_weather_broadcast = data['weather'][0]['main']
    if total_weather_broadcast in dict_of_wead_emo:
        total_weather = dict_of_wead_emo[total_weather_broadcast]
    else:
        total_weather = 'Just look out of the window'
    
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,\
        f'{datetime.now().strftime("%H:%M %d %B %Y")}\
        \nNow in Mocsow: {total_weather} and {temp_current}℃ \nFeels like: {feels_like}℃\
        \nWind speed: {wind_speed}m\h\nSunrise at {sunrise_t.strftime("%H:%M:%S")}\nSunset at {sunset_t.strftime("%H:%M:%S")}\
        \nMax temperature: {temp_max}℃\nMin temperature: {temp_min}℃\
        \n\nWish you a very sweet day!')
    
    

if __name__ == '__main__':
    executor.start_polling(dp)
 