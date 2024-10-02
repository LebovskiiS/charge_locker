from . import db
from app.cookies.create_cookies import create_cookies

def get_spots():
    return db.get_spots()


def book_spot_with_time(spot_id, selected_time):
    return db.book_spot_with_time(spot_id, selected_time)


