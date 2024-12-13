from werkzeug.utils import redirect
from flask import Flask, request
from functools import wraps
from .controllers import get_session_by_token_controller, is_available_controller
from datetime import datetime
from app.logs import logger
from app import db

def check_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.cookies.get('jwt')
        if get_session_by_token_controller(token):
            logger.debug('token found')
            return func(*args, **kwargs)
        else:
            logger.debug('token checked not found, return /spots')
            return redirect('/spots')

    return wrapped


def is_the_spot_available(func):
    def wrapped(spot_id=None, *args, **kwargs):
        if spot_id is None:
            spot_id = request.args.get('spot_id')
        if spot_id is None:
            json_data = request.get_json()
            if json_data:
                spot_id = json_data.get('spot_id')
        if is_available_controller(spot_id):
            return func(spot_id, *args, **kwargs)
        else:
            return redirect('/spots')
    return wrapped



def delete_old_sessions(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        db.delete_old_sessions()
        return func(*args, **kwargs)

    return wrapped


