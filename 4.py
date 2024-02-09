import telebot
import requests
import json

bot = telebot.TeleBot('***')
API = '***'


@bot.message_handlers(commands=['start'])
# декоратор запуска бота, обработка команд
def start(message):
    bot.send_message(message.chat.id, 'Привет, рад тебя видеть! Напиши название города.')


def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.ord/data/2.5/weather?q={city}&appid={API}&units=metric')
    # &units=metric - перевод в цельсии
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data['main']['temp']
        bot.reply_to(message, f'Температура в указанном городе: {data['main']['temp']} °C')
    else:
        bot.reply_to(message, 'Город указан неверно!')


bot.polling(non_stop=True)
