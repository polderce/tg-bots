import sqlite3
import telebot

bot = telebot.TeleBot('***')
name = None


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('miwabot.sql')
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), password varchar)""")
    # varchar - тип данных, 50 - длина
    conn.commit()
    # синхронизация изменений
    cur.close()
    # закрываем курсор
    conn.close()
    # закрываем соединение

    bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегестрируем! Введите ваше имя.')
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    password = message.text.strip
    conn = sqlite3.connect('miwabot.sql')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, password) VALUES ('%s', '%s')" % (name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, 'Пользователь зарагистрирован!', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
# func=lambda - анонимная ф-ция
def callback(call):
    conn = sqlite3.connect('miwabot.sql')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    user = cur.fetchall()

    info = ''
    for el in user:
        info += f'Имя: {el[1]}, пароль: {el[2]}\n'

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)


bot.polling(non_stop=True)
