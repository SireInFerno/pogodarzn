import requests
import schedule
import time
from datetime import datetime
import asyncio
from telegram import Bot
from telegram.constants import ParseMode

TELEGRAM_TOKEN = 'TGTOKEN'
CHAT_ID = ['', '', '', '']

OWM_API_KEY = '06108441159fd8c9e7543143452497fd'
CITY_ID = '500096'

def get_weather():
    url = f'http://api.openweathermap.org/data/2.5/forecast?id={CITY_ID}&appid={OWM_API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    
    forecast = {}
    for entry in data['list']:
        timestamp = entry['dt']
        hour = datetime.fromtimestamp(timestamp).hour
        if hour in [9, 12, 15, 18, 20, 21, 24]:
            forecast[hour] = entry['main']['temp']
    
    return forecast

async def send_weather():
    bot = Bot(token=TELEGRAM_TOKEN)
    weather = get_weather()
    message = "Сегодняшняя погода в Рязани:\n"
    for hour, temp in sorted(weather.items()):
        message += f"{hour}:00 - {temp}°C\n"

    
    for chat_id in CHAT_ID:
        await bot.send_message(chat_id=chat_id, text=message)


def job():
    asyncio.run(send_weather())

# Запланировать ежедневную отправку в 6:00 утра
schedule.every().day.at("06:00:00").do(job)

# Бесконечный цикл для выполнения задач
while True:
    schedule.run_pending()
    time.sleep(1)
