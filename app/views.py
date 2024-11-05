from .controllers import (main_controller, submit_controller,
                          get_session_by_token_controller, get_spot_info_by_id_controller, get_spot_info_by_token_controller)
from datetime import datetime
from flask import request, render_template, redirect
from . import db
from auth.jwt_token import create_token
from .decorators import check_token, is_the_spot_available


@check_token
def main_view():
    session = main_controller(request.cookies.get('jwt'))
    spot_id = session[1]
    start = session[2]
    end = session[3]
    floor = session[7]
    building = session[8]
    spot_number = session[9]


    return render_template('session_info.html',spot_id = spot_id, start = start, end= end,
                           floor= floor, building = building,
                           spot_number= spot_number
                           )


def get_spots_view():
    spots = db.get_available_spots()
    if spots:
        return render_template('available_spots.html', spots= spots)
    else:
        return render_template('no_available_spots.html')


# @is_the_spot_available
def choose_time_view(spot_id):
    spot_data = get_spot_info_by_id_controller(spot_id)
    building = spot_data[1]
    floor = spot_data[2]
    spot_number = spot_data[3]
    return render_template('choose_time.html',
                           building= building, spot_number= spot_number, floor = floor  , spot_id = spot_id)



# @is_the_spot_available
def submit_view():
    token = create_token()
    spot_id = request.form.get('spot_id')
    start = request.form.get('time_start')
    end = request.form.get('time_end')
    try:
        submit_controller(token, spot_id, start, end)
        resp = redirect('/')
        resp.set_cookie(key='jwt', value=token, max_age=60 * 60 * 16)
        return resp
    except Exception as e:
        return {'error': f'something went wrong: {e}'}



@check_token
def session_view():
    token = request.cookies.get('jwt')
    session_info = get_session_by_token_controller(token)  # id, spot_id, start, end, token
    spot_info = get_spot_info_by_token_controller(token)

    floor = spot_info[1]
    building = spot_info[2]
    spot_number = spot_info[3]
    start = datetime.strptime(session_info[2], '%Y-%m-%d %H:%M:%S')
    end = datetime.strptime(session_info[3], '%Y-%m-%d %H:%M:%S')


    return render_template(
        'session_info.html', start=start,
        end=end, floor=floor, building=building,
        spot_number=spot_number
    )
