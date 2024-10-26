from unittest import TestCase
from app import app, db
import os
from config import WORK_DIRECTORY

class TestMain(TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.client = app.test_client()
        cls.db = db


    def test_main_no_token(self):
        response = self.client.get('/')
        self.assertEqual(302,response.status_code )


    def test_main_token_exists(self):
        self.db.cursor.execute('INSERT INTO spots(floor, building, spot_number, is_available) VALUES (11,11,11,11)')
        self.db.connection.commit()
        spot_id = self.db.cursor.lastrowid
        self.db.book_spot('test_token',spot_id, 11,11)
        self.client.set_cookie('jwt', 'test_token')
        response = self.client.get('/')
        self.assertEqual(200,response.status_code)
        self.assertIn('Session Information', response.get_data(as_text=True))

    # @classmethod
    # def tearDownClass(cls):
    #     os.remove(WORK_DIRECTORY +'/charger_locker_database.db')




