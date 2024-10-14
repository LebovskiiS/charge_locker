from . import db

def main_controller(token):
        data = db.get_session_by_cookies(token)
        return data

def get_available_spots_controller():
        return db.get_available_spots()

def book_time_controller():
        db.return_token_if_exists()