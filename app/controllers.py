from . import db


def main_controller(token):
        session_info = db.get_session_by_token(token)
        spot_info = db.get_spot_info_by_token(token)
        return [*session_info, *spot_info]

def get_spots_controller():
        return db.get_spots()



def submit_controller(token, spot_id, start, end):
        return db.book_spot(token, spot_id, start, end)

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

def change_session_controller(token, new_end):
        db.change_booking(token,new_end)
        return 'ok'


# def get_session_by_token_controller(token):
#         return db.g

