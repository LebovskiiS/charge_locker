from unittest import TestCase

from flask import request

from app import app, db

class TestChooseTime(TestCase):
    @classmethod
    def setUp(cls):
        app.config['TESTING'] = True
        cls.client = app.test_client()
        cls.db = db

    def test_got_id_in_url(self):
        spot_id = self.db.add_new_spots(99,99,99)
        response = self.client.get(f'/time/{spot_id}')
        self.assertEqual(200, response.status_code)
        data = response.get_data(as_text=True)
        spot_number = self.db.cursor.execute(
            'SELECT spot_number FROM spots WHERE id = ?', [spot_id]
        ).fetchone()
        self.assertIn(spot_number, data)
