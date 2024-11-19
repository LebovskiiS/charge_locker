from datetime import datetime
from . import db

def main_controller(token):
    session_info = db.get_session_by_token(token)
    spot_info = db.get_spot_info_by_token(token)
    return [*session_info, *spot_info]

def book_spot(token, spot_id, start, end, uid):
    # Implementation of book_spot that ensures uid is non-null
    pass

def get_available_spots_controller():
    return db.get_available_spots()

def submit_controller(token, spot_id, start, end, uid):
    if not uid:
        uid = 0

    if not uid:
        uid = 0

    start_datetime = datetime.strptime(start, "%Y-%m-%d %I:%M %p")
    end_datetime = datetime.strptime(end, "%Y-%m-%d %I:%M %p")
    return db.book_spot(token, spot_id, start_datetime, end_datetime, uid)

def get_session_by_token_controller(token):
    return db.get_session_by_token(token)

def get_spot_info_by_id_controller(spot_id):
    return db.get_spot_info_by_id(spot_id)

def is_available_controller(spot_id):
    return db.is_available(spot_id)

def get_spot_info_by_token_controller(token):
    return db.get_spot_info_by_token(token)

def stop_booking_controller(token):
    db.stop_booking(token)
    return 'ok'

# def extend_booking_controller(token):
#     db.extend_booking()