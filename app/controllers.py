from . import db

def main_controller(token):
        data = db.get_session_by_token(token)
        return data

def get_available_spots_controller():
        return db.get_available_spots()



def submit_controller(token, spot_id, start, end):
        return db.book_spot(token, spot_id, start, end)

def get_session_by_token_controller(token):
        return db.get_session_by_token(token)


def get_spot_info_by_id_controller(spot_id):
        return db.get_spot_info_by_id(spot_id)