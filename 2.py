import telebot


bot = telebot.TeleBot('***')


@bot.message_handler(commands=['start'], content_types=['photo'])
# обработка команды start и других файлов (текст, видео, аудио и т.д.)
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    #  добавление кнопок над клавиатурой
    btn1 = telebot.types.KeyboardButton('Открыть браузер')
    markup.row(btn1)
    btn2 = telebot.types.KeyboardButton('Удалить фото')
    btn3 = telebot.types.KeyboardButton('Изменить текст')
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, 'Привет', reply_markup=markup)


def on_click(message):
    if message.text == 'Открыть браузер':
        bot.send_message(message.chat.id, 'Website is open')
    elif message.text == 'Удалить фото':
        bot.send_message(message.chat.id, 'Deleted')
    elif message.text == 'Изменить текст':
        bot.send_message(message.chat.id, 'Text edited')


def get_photo(message):
    markup = telebot.types.InlineKeyboardMarkup()
    # добавление кнопки под сообщением
    btn1 = telebot.types.InlineKeyboardButton('Открыть браузер', url='https://ya.ru')
    btn2 = telebot.types.InlineKeyboardButton('Удалить фото', callback_data='delete')
    btn3 = telebot.types.InlineKeyboardButton('Изменить текст', callback_data='edit')
    markup.row(btn1)
    # создание 1-го ряда с 1-ой кнопкой
    markup.row(btn2, btn3)
    # создание 2-го ряда с 2-мя кнопками
    bot.reply_to(message, 'Какое красивое фото!', reply_markup=markup)
    # ответ на фото и приклепление кнопок под ним


@bot.callback_query_handler(func=lambda callback: True)
# декоратор для работы кнопок
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
        # удаление сообщения по id предыдущего сообщения
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)
        # редактирование сообщения


bot.polling(none_stop=True)
