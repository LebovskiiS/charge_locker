from datetime import datetime
from flask import request, render_template, redirect
from .controllers import (
    main_controller, submit_controller,
    get_session_by_token_controller, get_spot_info_by_id_controller, get_spot_info_by_token_controller, stop_booking_controller)
from . import db
from auth.jwt_token import create_token
from .decorators import check_token, delete_old_sessions
from app.logs import loger


def time_to_db_format(date_str, time_str):
    datetime_obj = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %I:%M %p')
    return datetime_obj.strftime('%Y-%m-%d %I:%M %p')



def full_time_to_12_hour_format(datetime_str):
    datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %I:%M %p')
    return datetime_obj.strftime('%I:%M %p')


@delete_old_sessions
@check_token
def main_view():
    loger.debug('main func started with token')
    session = main_controller(request.cookies.get('jwt'))
    spot_id = session[1]
    start = session[2]
    end = session[3]
    floor = session[6]
    building = session[7]
    spot_number = session[8]
    print(f'floor:{floor}, building:{building}, '
          f'spot_number:{spot_number}, start:{start}, end:{end}')
    loger.warning('main rendering session_info.html')
    return render_template(
        'session_info.html', spot_id=spot_id, start=start, end=end,
        floor=floor, building=building, spot_number=spot_number
    )



def get_spots_view():
    spots = db.get_available_spots()
    if spots:
        loger.debug('returned spots')
        return render_template('available_spots.html', spots=spots)
    else:
        return render_template('no_available_spots.html')




def choose_time_view(spot_id):
    spot_data = get_spot_info_by_id_controller(spot_id)
    building = spot_data[1]
    floor = spot_data[2]
    spot_number = spot_data[3]
    return render_template(
        'choose_time.html', building=building, spot_number=spot_number,
        floor=floor, spot_id=spot_id
    )


@delete_old_sessions
def submit_view():
    token = create_token()
    spot_id = request.form.get('spot_id')
    start_12_hour = request.form.get('time_start')  # В 12-часовом формате ('4:30 PM')
    end_12_hour = request.form.get('time_end')  # В 12-часовом формате ('6:00 PM')

    # Создаем текущую дату для включения в datetime формат записи
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Преобразуем в формат для хранения в базе данных
    start_db_format = time_to_db_format(current_date, start_12_hour)
    end_db_format = time_to_db_format(current_date, end_12_hour)

    try:
        submit_controller(token, spot_id, start_db_format, end_db_format)
        resp = redirect('/')
        resp.set_cookie(key='jwt', value=token, max_age=60 * 60 * 16)
        return resp
    except Exception as e:
        return f'something went wrong: {e}'


@check_token
def session_view():
    token = request.cookies.get('jwt')
    session_info = get_session_by_token_controller(token)  # id, spot_id, start, end, token
    spot_info = get_spot_info_by_token_controller(token)

    floor = spot_info[2]
    building = spot_info[3]
    spot_number = spot_info[4]
    start = session_info[5]
    end = session_info[6]
    print(f'floor:{floor}, building:{building}, '
          f'spot_number:{spot_number}, start:{start}, end:{end}')
    return render_template(
        'session_info.html', start=start, end=end, floor=floor,
        building= building, spot_number= spot_number
    )


@check_token
def stop_booking_view():
    stop_booking_controller(request.cookies.get('jwt'))
    return redirect('/')


def info_view_en():
    return render_template('info_en.html')

def info_view_ch():
    return render_template('info_ch.html')

def info_view_ru():
    return render_template('info_ru.html')

def info_view_fa():
    return render_template('info_fa.html')

# @check_token
# def extend_time_view():
#     session = get_session_by_token_controller(request.cookies.get('jwt'))
#     spot = get_spot_info_by_token_controller(request.cookies.get('jwt'))
#     floor = spot[1]
#     building = spot[2]
#     spot_number = spot[3]
#     start = session[1]
#     end = session[2]
#     return render_template('extend_booking.html', floor= floor, building= building, spot_number= spot_number,
#                            start= start, end= end)
#

