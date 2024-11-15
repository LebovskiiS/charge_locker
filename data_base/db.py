
import psycopg2
from .scripts import sessions_db, spots_db, show_available_spots
from config import DB_NAME, DB_USER, DB_PASSWORD
dbname=DB_NAME,
user=DB_USER,
password=DB_PASSWORD,
host='localhost',
port='5432'



class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host='localhost',
            port='5432'
        )
        self.cursor = self.connection.cursor()
        self.create_tables()
        self.connection.commit()
        self.load_initial_spots()

    def load_initial_spots(self):
        self.add_new_spots(1, 1, 1)
        self.create_tables()
        self.connection.commit()
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

        # Methods some_code

    def create_tables(self):
        self.cursor.execute(spots_db)
        self.cursor.execute(sessions_db)
        self.connection.commit()





    def get_available_spots(self):
        self.cursor.execute(show_available_spots)
        available_spots = self.cursor.fetchall()
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
        self.cursor.execute('SELECT is_available FROM spots WHERE ID = %s', (spot_id,))
        data = self.cursor.fetchone()
        if data and data[0]:
            return True
        return False



    def get_spot_id(self, floor, building, spot_number):
        self.cursor.execute('SELECT ID FROM spots WHERE floor=%s AND building=%s AND spot_number=%s',
                             (floor, building, spot_number))
        spot_id = self.cursor.fetchone()
        return spot_id



    def book_spot(self, token, spot_id, start, end):
        self.cursor.execute('UPDATE spots SET is_available = 0 WHERE ID = %s', (spot_id,))
        self.connection.commit()
        self.cursor.execute(
            'INSERT INTO sessions (start, end, token, spot_id) '
            'VALUES (%s, %s, %s, %s)', (start, end, token, spot_id))
        self.connection.commit()
        self.cursor.execute('SELECT lastval()')
        return self.cursor.fetchone()[0]



    def return_token_if_exists(self, token):
        self.cursor.execute('SELECT token FROM sessions WHERE token = %s', (token,))
        cookies = self.cursor.fetchone()
        if cookies:
            return token
        else:
            return False



    def show_end_time(self, token):
        self.cursor.execute('SELECT end FROM sessions WHERE cookies = %s', (token,))
        end_time = self.cursor.fetchone()
        return end_time



    def add_new_spots(self, floor, building, spot_number):
        self.cursor.execute('INSERT INTO spots (floor, building, spot_number) VALUES (%s, %s, %s)',
                             (floor, building, spot_number))
        self.cursor.execute('SELECT lastval()')
        spot_id = self.cursor.fetchone()[0]
        return spot_id


    def stop_booking(self, token):
        self.cursor.execute('DELETE FROM sessions WHERE token = %s', (token,))
        self.cursor.execute(
            '''
            UPDATE spots
            SET is_available = 1
            WHERE ID IN (
                SELECT spot_id
                FROM sessions
                WHERE token = %s
            );
            ''', (token,)
        )
        self.connection.commit()
        return 'ok'



    def get_session_by_token(self, token):
        self.cursor.execute('SELECT * FROM sessions WHERE token = %s', [token])
        return self.cursor.fetchone()


    def get_spot_info_by_id(self, spot_id):
        self.cursor.execute('SELECT * FROM spots WHERE id = %s', [spot_id])
        return self.cursor.fetchone()


    def get_spot_info_by_token(self, token):
        self.cursor.execute(
            'SELECT * FROM spots JOIN sessions ON spots.id = sessions.spot_id WHERE token = %s',
            [token])
        return self.cursor.fetchone()




    def delete_old_sessions(self):
        try:
            self.cursor.execute('BEGIN;')


            self.cursor.execute(
                '''
                DELETE FROM sessions
                WHERE (end IS NOT NULL AND end < to_timestamp(EXTRACT(epoch FROM NOW()))) OR end IS NULL;
                '''
            )
            self.cursor.execute(
                '''
                UPDATE spots
                SET is_available = 1
                WHERE ID IN (
                    SELECT spot_id
                    FROM sessions
                    WHERE (end IS NOT NULL AND end < to_timestamp(EXTRACT(epoch FROM NOW()))) OR end IS NULL
                );
                '''
            )
            self.connection.commit()
        except psycopg2.Error as e:
            self.connection.rollback()
            print(f"An error occurred: {e}")

