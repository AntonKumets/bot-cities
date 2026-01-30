import telebot
from config import *
from logic import *
import os

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может показывать города на карте. Напиши /help для списка команд.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id,
        "Доступные команды:\n"
        "/start - приветствие\n"
        "/help - список команд\n"
        "/show_city  - показать город на карте\n"
        "/remember_city  - запомнить город\n"
        "/show_my_cities - показать все твои сохранённые города на карте")
    # Допиши команды бота


@bot.message_handler(commands=['show_city'])
def handle_show_city(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.send_message(
            message.chat.id,
            "Напиши город после команды, например: /show_city London"
        )
        return

    city_name = parts[1].strip()


@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    user_id = message.chat.id
    city_name = message.text.split()[-1]
    if manager.add_city(user_id, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    cities = manager.select_cities(message.chat.id)
    user_id = message.chat.id
    img_path = f"map_{user_id}_all.png"
    manager.create_grapf(img_path, cities)

    if os.path.exists(img_path):
        with open(img_path, "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="Твои города на карте")
        os.remove(img_path)


if __name__=="__main__":
    manager = DB_Map(DATABASE)
    bot.polling()
