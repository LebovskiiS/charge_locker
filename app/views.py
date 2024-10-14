from .controllers import main_controller, get_available_spots_controller
from flask import request, render_template, redirect, jsonify
from . import db
from datetime import datetime, timedelta
from auth.jwt_token import decode_token

from config import TEMPLATES_PATH
def main_view():
    if db.get_session_by_cookies(request.cookies.get('jwt')):
        session = main_controller(request.cookies.get('jwt'))
        session_info =  [{'id':session['id'], 'start':session['start'],
                  'end':session['end'], 'status':session['status']}]
        return render_template('/session_info.html', session_info= session_info)
    else:
        return redirect('/spots')


def get_spots_view():
    spots = get_available_spots_controller()
    if spots:
        return render_template('available_spots.html', spots= spots)
    else:
        return render_template('no_available_spots.html')



def book_time_view():
    token = request.cookies.get('jwt')

    if not token:
        return jsonify({'error': 'Токен отсутствует!'}), 401

    # Декодируем токен и получаем данные пользователя
    try:
        decoded_token = decode_token(token)
    except Exception as e:
        return jsonify({'error': str(e)}), 401

    spot_id = request.args.get('spot_id')
    booked_time = request.form['time']
    end_time = datetime.now() + timedelta(hours=int(booked_time))

    try:
        db.book_spot_with_time(spot_id, end_time)
        return jsonify({'message': f'Место {spot_id} успешно забронировано до {end_time}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


def submit_view():
    token = request.cookies.get('jwt')
    if not token:
        return jsonify({'error': 'Токен отсутствует!'}), 401

    spot_id = request.form.get('spot_id')
    booked_time = request.form.get('time')

    if spot_id and booked_time:
        response = book_time_view()
        return response
    else:
        return jsonify({'error': 'ID места и время обязательны!'}), 400