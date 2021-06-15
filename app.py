import telegram
import os
import datetime as dt
import time
import requests
import logging

from dotenv import load_dotenv

# Можно написать класс с методами.

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
WEATHER_API = os.getenv('WEATHER_API')

bot = telegram.Bot(token=TELEGRAM_TOKEN)

path = "https://api.openweathermap.org/data/2.5/"
excluded_params = "hourly,daily,minutely&units=metric&lang=ru"
text = 'доброе утро Коля!'


def weather_get(lat, lon):
    weath = requests.post(f"{path}onecall?lat={lat}&lon={lon}&exclude={excluded_params}&appid={WEATHER_API}").json()
    # temp = weath.get("current").get("temp")
    feel_like_temp = weath.get("current").get("feels_like")
    description = weath.get("current").get("weather")[0].get("description")
    return (f'сейчас на улице по ощущениям {feel_like_temp} градусов и {description}')


def send_message(message):
    return bot.send_message(chat_id=CHAT_ID, text=message)


def main():
    time_now = dt.datetime.now()
    hour = time_now.hour
    weath = weather_get(43.10562, 131.87353)

    while True:
        try:
            if hour == 15:
                send_message(text)
                send_message(weath)
                break
            time.sleep(60) # 2400
        except Exception as e:
            logging.exception(e, "Exception occurred")
            print(f'Бот упал с ошибкой: {e}')
            time.sleep(5)
            continue


if __name__ == '__main__':
    main()
