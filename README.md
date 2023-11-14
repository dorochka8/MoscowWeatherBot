# MoscowWeatherBot

I welcome everyone to use my source code to create own Weather Bot.

There are several things I direct for **all developers** for the moment.

# Creating your Application

1. [**Obtain your own token to access the HTTP API**](https://t.me/BotFather) for your application.
2. [**Obtain your own API key**](https://home.openweathermap.org/api_keys) to get current weather in any part of the world.
3. Please **do use** an individual file for all yous accesses, including your access to database (`config.py`).
4. Kindly **do use** the `aiogram` library for telegram bot, `python` for coding and `aiohttp` for requests.
   
# Guide

1. Clone the project from GitHub (*Windows compatibility*):

```
git clone --recursive -j8 https://github.com/dorochka8/MoscowWeatherBot
```
2. Install `requirements.txt` (directly from https://github.com/dorochka8/MoscowWeatherBot/blob/main/requirements.txt to get all the libraries that are used in the project, *VS Code compatibility*).
3. Adjust configuration parameters:
- Modify the values in `config.py`
- Modify the values in `main_bot.py` (token, str 14)
4. (Optional) Change the information you want to send to user in `main_weather.py`. According to json (str 19) choose the parameters you want to add or remove.
5. Start your Bot with running the `main_bot.py` file.
6. Start your Website on localhost with:
```
> py main_flask.py
```
  
# Tips

MoscowWeatherBot is used to build the Weather bot yourself. You will much more simplify your development by following the steps above.

Moreover to start a World-wide Weather Bot, follow these steps:
1. Import all needed packages, Classes 
> MemoryStorage from aiogram.contrib.fsm_storage.memory
>> FSMContext from aiogram.dispatcher
>>> StatesGroup from aiogram.dispatcher.filters.state
2. Ask a user about the town he is interested in and this message will handle from user because of a StatesGroup Class.
3. Enjoy!
