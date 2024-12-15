import os
import psycopg2
from psycopg2.extras import RealDictCursor
from .scripts import sessions_db, spots_db, show_spots
from config import DATABASE_URL
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
        self.connection = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
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
        # Создаём таблицы для PostgreSQL
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS spots (
                ID SERIAL PRIMARY KEY,
                floor INTEGER NOT NULL,
                building INTEGER DEFAULT NULL,
                spot_number INTEGER NOT NULL,
                is_available BOOLEAN DEFAULT TRUE
            );
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                ID SERIAL PRIMARY KEY,
                spot_id INTEGER NOT NULL,
                start TIMESTAMP NOT NULL,
                end TIMESTAMP DEFAULT NULL,
                token TEXT NOT NULL,
                FOREIGN KEY(spot_id) REFERENCES spots(ID) ON DELETE CASCADE
            );
            """
        )
        self.connection.commit()

    def get_all_spots(self):
        self.cursor.execute(
            """
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
                CASE WHEN sessions.end IS NULL THEN 1 ELSE 0 END, sessions.end ASC;
            """
        )
        return self.cursor.fetchall()

    def is_available(self, spot_id):
        self.cursor.execute('SELECT is_available FROM spots WHERE ID = %s', (spot_id,))
        data = self.cursor.fetchone()
        return data['is_available'] if data else False

    def check_spot_exists(self, floor, building, spot_number):
        self.cursor.execute(
            'SELECT EXISTS(SELECT 1 FROM spots WHERE floor=%s AND building=%s AND spot_number=%s)',
            (floor, building, spot_number)
        )
        return self.cursor.fetchone()['exists']

    def get_spot_id(self, floor, building, spot_number):
        self.cursor.execute(
            'SELECT ID FROM spots WHERE floor=%s AND building=%s AND spot_number=%s',
            (floor, building, spot_number)
        )
        return self.cursor.fetchone()

    def book_spot(self, token, spot_id, start, end):
        try:
            self.cursor.execute('UPDATE spots SET is_available = FALSE WHERE ID = %s', (spot_id,))
            self.cursor.execute(
                'INSERT INTO sessions (start, end, token, spot_id) VALUES (%s, %s, %s, %s)',
                (start, end, token, spot_id)
            )
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Error booking spot: {e}")
            raise e

    def return_token_if_exists(self, token):
        self.cursor.execute('SELECT token FROM sessions WHERE token = %s', (token,))
        return self.cursor.fetchone()

    def delete_old_sessions(self):
        try:
            logger.info("Started cleaning up outdated sessions")
            self.cursor.execute(
                """
                DELETE FROM sessions
                WHERE end < now()
                RETURNING spot_id;
                """
            )
            expired_sessions = self.cursor.fetchall()
            for session in expired_sessions:
                self.cursor.execute(
                    'UPDATE spots SET is_available = TRUE WHERE ID = %s',
                    (session['spot_id'],)
                )
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Error deleting old sessions: {e}")
            raise e