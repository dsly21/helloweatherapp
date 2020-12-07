from dotenv import load_dotenv
import telegram
import os
import datetime as dt
import time
import requests
import logging

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
WEATHER_API = os.getenv('WEATHER_API')
text = 'доброе утро Коля!'
bot = telegram.Bot(token=TELEGRAM_TOKEN)


def weather_get(lat, lon):
    # поправить по pep8
    weath = requests.post(f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=hourly,daily,minutely&units=metric&lang=ru&appid={WEATHER_API}").json()
    temp = weath.get("current").get("temp")
    return (f'сейчас {temp} градусов') #пока не ясно как вывести несколько нужных мне параметров


def send_message(message):
    return bot.send_message(chat_id=CHAT_ID, text=message)


def main():
    time_now = dt.datetime.now()
    hour = time_now.hour
    weath = weather_get(43.10562, 131.87353)

    while True:
        try:
            if hour == 13:
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
