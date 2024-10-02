import sqlite3
from app.cookies.create_cookies import create_cookies
from flask import request

from .scripts import spots_db, sessions_db, users_db, show_available_spots



class Database:
    def __init__(self):
        self.connection = sqlite3.connect('./app/database/data_base.db', check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute(spots_db)
        self.cursor.execute(sessions_db)
        self.cursor.execute(users_db)
        self.connection.commit()  # Коммитим изменения после создания таблиц

    def get_spots(self):
        cookies = request.cookies
        if self.is_cookies_exists(cookies):
            available_spots = self.cursor.execute(show_available_spots).fetchall()
            print(available_spots)
            spots_to_return = []
            for spot in available_spots:
                spots_to_return.append({
                    'ID': spot[0],
                    'floor': spot[1],
                    'building': spot[2],
                    'spot_number': spot[3],
                    'is_available': spot[4]
                })
            return spots_to_return
        else:
            return self.show_end_time(cookies)

    def is_available(self, spot_id):
        self.cursor.execute('SELECT is_open FROM spots WHERE ID = ?', (spot_id,))
        data = self.cursor.fetchone()
        if data and data[0]:
            return True
        return False

    def get_spot_id(self, floor, building, spot_number):
        spot_id = self.cursor.execute('SELECT ID FROM spots WHERE floor=? AND building=? AND spot_number=?',
                                      (floor, building, spot_number)).fetchone()
        return spot_id

    def book_spot_with_time(self, spot_id, selected_time):
        if self.is_available(spot_id):
            self.cursor.execute('UPDATE spots SET is_open = ?, booked_time = ? WHERE ID = ?',
                                (False, selected_time, spot_id))
            self.connection.commit()
            return 'ok'
        else:
            raise ExceptionSlotIsntAvailable(f"Spot {spot_id} is not available for booking.")


    def is_cookies_exists(self, cookies):
        cookies = self.cursor.execute('FROM sessions SELECT cookies  WHERE cookies = ?',(cookies,))
        if cookies:
            return True
        else:
            return False

    def show_end_time(self, cookies):
        end_time = self.cursor.execute('FROM sessions SELECT end WHERE cookies = ?', (cookies,))
        return end_time

    def add_new_spots(self, floor, building, spot_number):
        self.cursor.execute('INSERT INTO spots (floor, building, spot_number')
        self.connection.commit()
        spot_id = self.cursor.lastrowid
        return spot_id

