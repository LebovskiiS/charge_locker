import sqlite3
from .scripts import sessions_db, spots_db, show_available_spots
from config import WORK_DIRECTORY


class Database:
    _instance = None


    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls, *args, **kwargs)
        return cls._instance


    def __init__(self):
        self.connection = sqlite3.connect(WORK_DIRECTORY +'/charger_locker_database.db', check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()


    def create_tables(self):
        self.cursor.execute(spots_db)
        self.cursor.execute(sessions_db)
        self.connection.commit()
        self.cursor.execute('INSERT INTO spots (floor, building, spot_number, is_available) VALUES '
                            '(1, 3, 13, 1)')
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
        self.cursor.execute('SELECT is_available FROM spots WHERE ID = ?', (spot_id,))
        data = self.cursor.fetchone()
        if data and data[0]:
            return True
        return False


    def get_spot_id(self, floor, building, spot_number):
        spot_id = self.cursor.execute('SELECT ID FROM spots WHERE floor=? AND building=? AND spot_number=?',
                                      (floor, building, spot_number)).fetchone()
        return spot_id


    def book_spot(self, token, spot_id, start, end):
        self.cursor.execute('UPDATE spots SET is_available = 0 WHERE ID = ?', (spot_id,))
        self.connection.commit()
        self.cursor.execute(
            'INSERT INTO sessions (start, end, token, spot_id) '
            'VALUES (?, ?, ?, ?)', (start, end, token, spot_id))
        self.connection.commit()
        return self.cursor.lastrowid


    def return_token_if_exists(self, token):
        data = self.cursor.execute('SELECT token FROM sessions WHERE token = ?', (token,))
        cookies = data.fetchone()
        if cookies:
            return token
        else:
            return False

    def show_end_time(self, token):
        end_time = self.cursor.execute('SELECT end FROM sessions WHERE cookies = ?', (token,))
        return end_time


    def add_new_spots(self, floor, building, spot_number):
        self.cursor.execute('INSERT INTO spots (floor, building, spot_number) VALUES (?, ?, ?)',
                            (floor, building, spot_number))
        self.connection.commit()
        spot_id = self.cursor.lastrowid
        return spot_id


    def stop_booking(self, token):
        self.cursor.execute('DELETE FROM sessions WHERE token = ?', (token,))
        self.connection.commit()
        self.cursor.execute(
            '''
            UPDATE spots
            SET is_available = 0
            FROM sessions
            WHERE sessions.token = ? AND sessions.spot_id = spots.id
            ''',
            [token]
        )
        return 'ok'


    def get_session_by_token(self, token):
        self.cursor.execute('SELECT * FROM sessions WHERE token = ?', [token])
        return self.cursor.fetchone()

    def get_spot_info_by_id(self, spot_id):
        self.cursor.execute('SELECT * FROM spots WHERE id = ?', [spot_id])
        return self.cursor.fetchone()

    def get_spot_info_by_token(self, token):
        self.cursor.execute(
            'SELECT * FROM spots JOIN sessions ON spots.id = sessions.spot_id WHERE token = ?',
            [token])
        return self.cursor.fetchone()





    # def extend_session(self, token,time):
