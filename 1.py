import telebot

bot = telebot.TeleBot('***')

"""
@bot.message.handler(commands=['site', 'website']) - пример открытия сайта
def site(message):
    webbrowser.open('url сайта')
"""


@bot.message_handlers(commands=['start', 'hello', 'main'])
# декоратор запуска бота, обработка команд
def main(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')
    # сообщение после запуска бота, firs_name - Имя, last_name - Фамилия


@bot.message_handlers(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, '<b>Помощь скоро будет доступна!<b>')

'''
<b></b> - жирный шрифт
<em></em> - курсив        html-теги
<u></u> - подчеркивание 
'''

@bot.message_handler()
# обработка всех данных от пользователя
def info(message):
    if message.text.lower() == 'привет':
        # lower - привод всего текста в нижний регистр, чтобы бот понимал команды
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}.')


bot.polling(none_stop=True)
# работа бота безперерывно, можно bot.infinity.polling()
