import sqlite3
from config import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


class DB_Map():
    def __init__(self, database):
        self.database = database
    
    def create_user_table(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users_cities (
                                user_id INTEGER,
                                city_id TEXT,
                                FOREIGN KEY(city_id) REFERENCES cities(id)
                            )''')
            
            conn.execute('''CREATE TABLE IF NOT EXISTS user_settings (
                                user_id INTEGER PRIMARY KEY,
                                marker_color TEXT DEFAULT 'red'
                            )''')
            conn.commit()

    def add_city(self, user_id, city_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM cities WHERE city=?", (city_name,))
            city_data = cursor.fetchone()
            if city_data:
                city_id = city_data[0]  
                cursor.execute("SELECT 1 FROM users_cities WHERE user_id = ? AND city_id = ?", (user_id, city_id))
                if not cursor.fetchone():
                    conn.execute('INSERT INTO users_cities VALUES (?, ?)', (user_id, city_id))
                conn.commit()
                return 1
            else:
                return 0

            
    def select_cities(self, user_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT cities.city 
                            FROM users_cities  
                            JOIN cities ON users_cities.city_id = cities.id
                            WHERE users_cities.user_id = ?''', (user_id,))

            cities = [row[0] for row in cursor.fetchall()]
            return cities


    def get_coordinates(self, city_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT lat, lng
                            FROM cities  
                            WHERE city = ?''', (city_name,))
            coordinates = cursor.fetchone()
            return coordinates

    def get_marker_color(self, user_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT marker_color FROM user_settings WHERE user_id = ?''', (user_id,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                conn.execute('INSERT INTO user_settings (user_id, marker_color) VALUES (?, ?)', (user_id, 'red'))
                conn.commit()
                return 'red'

    def set_marker_color(self, user_id, color):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''INSERT OR REPLACE INTO user_settings (user_id, marker_color) 
                            VALUES (?, ?)''', (user_id, color))
            conn.commit()

    def create_grapf(self, path, cities, marker_color='red'):
        fig = plt.figure(figsize=(10, 6))
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.coastlines()
        ax.stock_img()
        
        for city in cities:
            coords = self.get_coordinates(city)
            if coords:
                lat, lng = coords
                ax.plot(lng, lat, marker_color + 'o', markersize=8, transform=ccrs.PlateCarree())
                ax.text(lng + 1, lat + 1, city, transform=ccrs.PlateCarree(), fontsize=9)
        
        plt.savefig(path)
        plt.close()
        
    def draw_distance(self, city1, city2):
        pass


    def get_cities_by_country(self, country):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT city 
                            FROM cities  
                            WHERE country = ? 
                            ORDER BY city''', (country,))
            cities = [row[0] for row in cursor.fetchall()]
            return cities

if __name__=="__main__":
    
    m = DB_Map(DATABASE)
    m.create_user_table()