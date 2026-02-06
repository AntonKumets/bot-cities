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
        "/show_city [город] - показать город на карте\n"
        "/remember_city [город] - запомнить город\n"
        "/show_my_cities - показать все твои сохранённые города на карте\n"
        "/clear_cities - удалить все сохранённые города\n"
        "/list_cities - список сохранённых городов")

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
    coords = manager.get_coordinates(city_name)
    
    if coords:
        lat, lng = coords
        user_id = message.chat.id
        img_path = f"map_{user_id}_single.png"
        
        fig = plt.figure(figsize=(8, 6))
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.coastlines()
        ax.stock_img()
        ax.plot(lng, lat, 'ro', markersize=12, transform=ccrs.PlateCarree())
        ax.text(lng + 1, lat + 1, city_name, transform=ccrs.PlateCarree(), fontsize=11, fontweight='bold')
        
        plt.savefig(img_path)
        plt.close()
        
        with open(img_path, "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption=f"Город: {city_name}\nКоординаты: {lat}, {lng}")
        os.remove(img_path)
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.send_message(
            message.chat.id,
            "Напиши город после команды, например: /remember_city Moscow"
        )
        return
    
    user_id = message.chat.id
    city_name = parts[1].strip()
    if manager.add_city(user_id, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    cities = manager.select_cities(message.chat.id)
    
    if not cities:
        bot.send_message(message.chat.id, "У тебя нет сохранённых городов. Используй /remember_city чтобы добавить город.")
        return
    
    user_id = message.chat.id
    img_path = f"map_{user_id}_all.png"
    manager.create_grapf(img_path, cities)

    if os.path.exists(img_path):
        with open(img_path, "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption=f"Твои города на карте ({len(cities)} городов)")
        os.remove(img_path)

@bot.message_handler(commands=['list_cities'])
def handle_list_cities(message):
    cities = manager.select_cities(message.chat.id)
    
    if not cities:
        bot.send_message(message.chat.id, "У тебя нет сохранённых городов.")
        return
    
    cities_list = "\n".join([f"• {city}" for city in cities])
    bot.send_message(message.chat.id, f"Твои сохранённые города:\n{cities_list}")

@bot.message_handler(commands=['clear_cities'])
def handle_clear_cities(message):
    user_id = message.chat.id
    conn = sqlite3.connect(DATABASE)
    with conn:
        conn.execute('DELETE FROM users_cities WHERE user_id = ?', (user_id,))
        conn.commit()
    bot.send_message(message.chat.id, "Все твои города удалены!")


if __name__=="__main__":
    manager = DB_Map(DATABASE)
    bot.polling()