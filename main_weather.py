import requests
from datetime import datetime
from pprint import pprint
from config import o_weather_token

def wot_is_d_weather(o_weather_token):
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
    pprint(data)

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
    
    
    print(f'{datetime.now().strftime("%H:%M %d %B %Y")}\
        \nNow in Mocsow: {total_weather} and {temp_current}℃ \nFeels like: {feels_like}℃\
        \nWind speed: {wind_speed}m\h\nSunrise at {sunrise_t.strftime("%H:%M:%S")}\nSunset at {sunset_t.strftime("%H:%M:%S")}\
        \nMax temperature: {temp_max}℃\nMax temperature: {temp_min}℃\
        \nWish you a nice day!')

def work_func():
    wot_is_d_weather(o_weather_token)

if __name__ == '__main__':
    work_func()