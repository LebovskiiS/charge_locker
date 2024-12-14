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
        self.connection = sqlite3.connect(WORK_DIRECTORY + '/charger_locker_database.db', check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()
        self.connection.commit()
        self.delete_old_sessions()
        spots = self.cursor.execute(show_spots).fetchall()
        if spots:
            logger.debug('Spots already exist')
        else:
            self.create_spots()
            logger.debug('Spots created')

    def create_spots(self):
        spot_data = [
            (1, 1, [1, 2, 3]),
            (2, 1, [1, 2, 3, 4]),
            (3, 1, [1, 2, 3, 4]),
            (4, 1, [1, 2, 3, 4]),
            (5, 1, [1, 2, 3, 4, 5, 6]),
            (2, 2, [1, 2]),
            (3, 2, [1, 2]),
            (4, 2, [1, 2]),
            (5, 2, [1, 2])
        ]
        for floor, building, spots in spot_data:
            for spot_number in spots:
                self.add_new_spots(floor, building, spot_number)

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
                sessions.end AS end_time
            FROM 
                spots
            LEFT JOIN 
                sessions ON spots.id = sessions.spot_id
            ORDER BY 
                CASE WHEN sessions.end IS NULL THEN 1 ELSE 0 END, sessions.end ASC; -- Null всегда в конец
        """).fetchall()

        spots_to_return = []
        for spot in results:
            readable_end_time = None
            if spot[5]:  # Проверяем значение UNIX timestamp
                try:
                    readable_end_time = datetime.fromtimestamp(spot[5]).strftime('%Y-%m-%d %I:%M %p')
                except (ValueError, OSError) as e:  # Если timestamp недействителен
                    logger.error(f"Invalid timestamp: {spot[5]} for spot ID {spot[0]}. Error: {e}")
                    readable_end_time = None

            spots_to_return.append({
                'ID': spot[0],
                'floor': spot[1],
                'building': spot[2],
                'spot_number': spot[3],
                'is_available': spot[4],
                'end_time': readable_end_time  # Преобразованное время
            })
        return spots_to_return

    def is_available(self, spot_id):
        self.cursor.execute('SELECT is_available FROM spots WHERE ID = ?', (spot_id,))
        data = self.cursor.fetchone()
        if data and data[0]:
            return True
        return False

    def check_spot_exists(self, floor, building, spot_number):
        result = self.cursor.execute(
            'SELECT EXISTS(SELECT 1 FROM spots WHERE floor=? AND building=? AND spot_number=?)',
            (floor, building, spot_number)
        ).fetchone()
        return result[0] == 1

    def get_spot_id(self, floor, building, spot_number):
        spot_id = self.cursor.execute('SELECT ID FROM spots WHERE floor=? AND building=? AND spot_number=?',
                                      (floor, building, spot_number)).fetchone()
        return spot_id

    def book_spot(self, token, spot_id, start, end):
        try:
            start_timestamp = int(datetime.strptime(start, '%Y-%m-%d %I:%M %p').timestamp())
            end_timestamp = int(datetime.strptime(end, '%Y-%m-%d %I:%M %p').timestamp())

            # Обновляем статус доступности спота и создаем бронирование
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
        try:
            data = self.cursor.execute('SELECT token FROM sessions WHERE token = ?', (token,))
            cookies = data.fetchone()
            if cookies:
                return token
            return False
        except sqlite3.Error as e:
            logger.error(f"Error fetching token: {e}")
            raise

    def show_end_time(self, token):
        try:
            end_time = self.cursor.execute('SELECT end FROM sessions WHERE token = ?', (token,)).fetchone()
            if end_time:
                return full_time_to_12_hour_format(datetime.fromtimestamp(end_time[0]).strftime('%Y-%m-%d %I:%M %p'))
            return None
        except sqlite3.Error as e:
            logger.error(f"Error fetching end time for token: {e}")
            raise

    def add_new_spots(self, floor, building, spot_number):
        if not self.check_spot_exists(floor, building, spot_number):
            self.cursor.execute('INSERT INTO spots (floor, building, spot_number) VALUES (?, ?, ?)',
                                (floor, building, spot_number))
            self.connection.commit()
            spot_id = self.cursor.lastrowid
            return spot_id
        logger.debug(f"Spot already exists: floor={floor}, building={building}, spot_number={spot_number}")
        return None

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
            logger.info("Started cleaning up outdated sessions")

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
