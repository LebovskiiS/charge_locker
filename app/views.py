from .controllers import main_controller, submit_controller, get_session_by_token_controller,get_spot_info_by_id_controller
from flask import request, render_template, redirect
from . import db
from auth.jwt_token import create_token


def main_view():
    session_token = get_session_by_token_controller(request.cookies.get('jwt'))
    if session_token:
        session = main_controller(request.cookies.get('jwt'))
        session_info =  {'id':session[0], 'start':session[1],
                  'end':session[2], 'status':session[3]}
        return render_template('session_info.html', session_info= session_info)
    else:
        return redirect('/spots')


def get_spots_view():
    spots = db.get_available_spots()
    if spots:
        return render_template('available_spots.html', spots= spots)
    else:
        return render_template('no_available_spots.html')



def book_time_view(spot_id):
    spot_data = get_spot_info_by_id_controller(spot_id)
    building = spot_data[1]
    floor = spot_data[2]
    spot_number = spot_data[3]
    return render_template('book_time.html',
                           building= building, spot_number= spot_number, floor = floor)




def submit_view():
    token = create_token()
    spot_id = request.args.get('spot_id')
    start = request.args.get('time_start')
    end = request.args.get('time_end')
    try:
        submit_controller(token, spot_id, start, end)
        resp = redirect('/')
        resp.set_cookie(key='jwt', value=token, max_age=60 * 60 * 16)
        return resp
    except Exception as e:
        return {'error': f'something went wrong: {e}'}





