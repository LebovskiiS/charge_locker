import sqlite3
from .scripts import sessions_db, spots_db, show_spots
from config import WORK_DIRECTORY
from app.logs import logger
from datetime import datetime

def full_time_to_12_hour_format(datetime_str):
    datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %I:%M %p')
    return datetime_obj.strftime('%I:%M %p')



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
        self.connection.commit()
        self.delete_old_sessions()
        spots_created = 0
        if spots_created == 0:
            self.create_spots()
            self.connection.commit()
            spots_created += 1
        else:
            logger.debug("Spots already created")
            pass

    def create_spots(self):
        self.add_new_spots(1, 1, 1)
        self.add_new_spots(1, 1, 2)
        self.add_new_spots(1, 1, 3)
        self.add_new_spots(2, 1, 1)
        self.add_new_spots(2, 1, 2)
        self.add_new_spots(2, 1, 3)
        self.add_new_spots(2, 1, 4)
        self.add_new_spots(3, 1, 1)
        self.add_new_spots(3, 1, 2)
        self.add_new_spots(3, 1, 3)
        self.add_new_spots(3, 1, 4)
        self.add_new_spots(4, 1, 1)
        self.add_new_spots(4, 1, 2)
        self.add_new_spots(4, 1, 3)
        self.add_new_spots(4, 1, 4)
        self.add_new_spots(5, 1, 1)
        self.add_new_spots(5, 1, 2)
        self.add_new_spots(5, 1, 3)
        self.add_new_spots(5, 1, 4)
        self.add_new_spots(5, 1, 5)
        self.add_new_spots(5, 1, 6)
        self.add_new_spots(2, 2, 1)
        self.add_new_spots(2, 2, 2)
        self.add_new_spots(3, 2, 1)
        self.add_new_spots(3, 2, 2)
        self.add_new_spots(4, 2, 1)
        self.add_new_spots(4, 2, 2)
        self.add_new_spots(5, 2, 1)
        self.add_new_spots(5, 2, 2)

    def create_tables(self):
        self.cursor.execute(spots_db)
        self.cursor.execute(sessions_db)
        self.connection.commit()

    def get_all_spots(self):
        results = self.cursor.execute("""
            SELECT 
                spots.id AS spot_id,
                spots.floor, 
                spots.building, 
                spots.spot_number, 
                spots.is_available,
                sessions.end AS end_time  -- `end_time` сохраняется как INTEGER (UNIX timestamp)
            FROM 
                spots
            LEFT JOIN 
                sessions ON spots.id = sessions.spot_id
            ORDER BY 
                sessions.end ASC;
        """).fetchall()

        spots_to_return = []
        for spot in results:
            spots_to_return.append({
                'ID': spot[0],
                'floor': spot[1],
                'building': spot[2],
                'spot_number': spot[3],
                'is_available': spot[4],
                # Передаем `end_time` напрямую из базы (INTEGER)
                'end_time': spot[5]
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
        try:
            start_timestamp = int(datetime.strptime(start, '%Y-%m-%d %I:%M %p').timestamp())
            end_timestamp = int(datetime.strptime(end, '%Y-%m-%d %I:%M %p').timestamp())

            self.cursor.execute('UPDATE spots SET is_available = 0 WHERE ID = ?', (spot_id,))
            self.cursor.execute(
                'INSERT INTO sessions (start, end, token, spot_id) VALUES (?, ?, ?, ?)',
                (start_timestamp, end_timestamp, token, spot_id)
            )
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            self.connection.rollback()
            logger.error(f"Error booking spot: {e}")
            raise e



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
        try:
            # Получаем ID спота
            spot_id = self.cursor.execute(
                'SELECT spot_id FROM sessions WHERE token = ?',
                (token,)
            ).fetchone()

            if not spot_id:
                logger.debug(f"No session found for token: {token}")
                return 'not found'

            # Обновляем доступность спота и удаляем сессию в одной транзакции
            self.cursor.execute(
                'UPDATE spots SET is_available = 1 WHERE ID = ?',
                (spot_id[0],)
            )
            self.cursor.execute('DELETE FROM sessions WHERE token = ?', (token,))
            self.connection.commit()
            logger.debug(f"Spot {spot_id[0]} released and session deleted for token: {token}")
            return 'ok'
        except sqlite3.Error as e:
            self.connection.rollback()
            logger.error(f"Error stopping booking: {e}")
            return 'error'


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

    def delete_old_sessions(self):
        try:
            logger.debug("Starting to delete old sessions")

            # Удаляем сессии с устаревшей датой `end`
            expired_sessions = self.cursor.execute(
                "SELECT id, spot_id FROM sessions WHERE end < strftime('%s', 'now')"
            ).fetchall()

            if not expired_sessions:
                logger.debug("No expired sessions found.")
                return

            # Удаляем старые записи сессий
            self.cursor.executemany(
                'DELETE FROM sessions WHERE id = ?',
                [(session[0],) for session in expired_sessions]
            )

            # Обновляем доступность соответствующих спотов
            for session in expired_sessions:
                self.cursor.execute(
                    'UPDATE spots SET is_available = 1 WHERE id = ?',
                    (session[1],)
                )

            self.connection.commit()
            logger.debug(f"{len(expired_sessions)} expired sessions deleted.")
        except sqlite3.Error as e:
            self.connection.rollback()
            logger.error(f"Error deleting old sessions: {e}")


    




