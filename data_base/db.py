import sqlite3
from .scripts import sessions_db, spots_db, show_available_spots


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('./data_base/charger_locker_database.db', check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()


    def create_tables(self):
        self.cursor.execute(spots_db)
        self.cursor.execute(sessions_db)
        self.connection.commit()


    def get_available_spots(self):
        available_spots = self.cursor.execute(show_available_spots).fetchall()
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


    def book_spot_with_time(self, spot_id, end_time):
        if self.is_available(spot_id):
            self.cursor.execute('UPDATE spots SET is_open = 0, WHERE ID = ?',
                                [spot_id])
            self.connection.commit()
            self.cursor.execute('UPDATE sessions SET start = ?, end = ?, status = ?',
                                [CURRENT_TIME, end_time, 1])
            self.connection.commit()
            return 'ok'
        else:
            raise Exception(f"Spot {spot_id} is not available for booking.")


    def is_cookies_exists(self, cookies):
        data = self.cursor.execute('SELECT cookies FROM sessions WHERE cookies = ?', (cookies,))
        cookies = data.fetchone()
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


    def delete_session_by_cookies(self, cookies):
        self.cursor.execute('DELETE FROM sessions WHERE cookies = ?', (cookies,))
        self.connection.commit()
        return 'ok'


    def get_session_by_cookies(self, cookies):
        self.cursor.execute(
            'SELECT sessions.start, sessions.end, spots.floor, spots.spot_number '
            'FROM sessions JOIN spots ON sessions.ID = spots.ID '
            'WHERE sessions.cookies = ?',
            (cookies,))
        return self.cursor.fetchall()