from unittest import TestCase
from app import app, db

class TestGetSpots(TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.client = app.test_client()
        cls.db = db


    def test_spots_exists(self):
        for spot in range(1,51):
            self.db.add_new_spots(1,1,spot)
        response = self.client.get('/spots')
        self.assertEqual(200,response.status_code)
        markup = response.get_data(as_text= True)
        result = markup.count('btn-primary')
        self.assertEqual(50,result)



