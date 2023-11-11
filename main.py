import json
import re
from telebot import types
import telebot
import psycopg2
from config import host, user, password, db_name

bot_token = '6859558715:AAFEZ3Qu3TMVi25L7jSObRvnOpfG1OSITDA'
bot = telebot.TeleBot(bot_token)

connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
cursor = connection.cursor()


def show_options(user_id):
    query = f"SELECT user_id, options FROM data_of;"
    cursor.execute(query)
    rows = cursor.fetchall()
    for i in range(len(rows)):
        bot.send_message(user_id, str(rows[int(i)]))
    bot.send_message(user_id, "Введите id пользователя и новый трекер:")






@bot.message_handler(commands=['IqbaXZ8BpRbAdnt'])
def starter(message):
    user_id = message.chat.id
    show_options(user_id)

@bot.message_handler(func=lambda message: True)
def handle_edit(message):
    admin_id = message.chat.id
    data_list = message.text.split()
    user_id = data_list[0] if len(data_list) > 0 else None
    option = data_list[1] if len(data_list) > 1 else None

    if user_id and option:
        try:
            # Получение текущего значения JSON
            query = f"SELECT options FROM data_of WHERE user_id = {user_id};"
            cursor.execute(query)
            result = cursor.fetchone()

            if result:
                json_data = result[0]
                json_obj = json_data

                # Добавление новой пары ключ-значение
                json_obj[option] = 0

                # Преобразование обратно в JSON-строку
                updated_json = json.dumps(json_obj)

                # Обновление значения в базе данных
                query_update = f"UPDATE data_of SET options = '{updated_json}' WHERE user_id = {user_id};"
                cursor.execute(query_update)
                connection.commit()

                bot.send_message(admin_id, f"Добавлена новая пара в JSON для user_id {user_id}, option {option}.")
            else:
                bot.send_message(admin_id, f"Нет данных для user_id {user_id}.")
        except Exception as ex:
            print(f"Error: {ex}")








# Запускаем бота
bot.polling(none_stop=True)
