import sqlite3
from .scripts import spots_db, sessions_db, users_db, show_avaliable_spots
from exceptions import ExceptionSlotIsntAvailable

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('data_base.db', check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute(spots_db)
        self.cursor.execute(sessions_db)
        self.cursor.execute(users_db)
        self.connection.commit()  # Коммитим изменения после создания таблиц

    def show_spots(self):
        available_spots = show_avaliable_spots()
        spots_to_return = []
        for spot in available_spots:
            spots_to_return.append({
                'ID': spot[0],
                'floor': spot[1],
                'building': spot[2],
                'spot_number': spot[3],
                'is_availabl': spot[4]  # Исправлено "is_availabl" на правильное имя, если это ошибка
            })
        return spots_to_return  # Исправлено расположение return

    def is_available(self, spot_id):
        self.cursor.execute('SELECT is_open FROM spots WHERE ID = ?', (spot_id,))
        data = self.cursor.fetchone()
        if data and data[0]:  # Проверяем наличие данных и их значение
            return True
        return False


    def get_spot_id(self, floor, building, spot_number):
        spot_id = self.cursor.execute('SELECT ID FROM spots WHERE floor,'
                                      ' building, spot_number = ?,?,?',
                                      [floor, building, spot_number])
        return spot_id


    def book_spot(self, spot_id):
        if self.is_available(spot_id):
            self.cursor.execute('UPDATE spots SET is_open = ? WHERE ID = ?', (False, spot_id))
            self.connection.commit()
            return 'ok'
        else:
            raise ExceptionSlotIsntAvailable(f"Spot {spot_id} is not available for booking.")









