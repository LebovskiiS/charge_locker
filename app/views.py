from controllers import main_controller, get_available_spots_controller
from flask import request, render_template, redirect
from . import db

def main_view():
    if db.get_session_by_cookies(request.cookies.get('cookies')):
        session = main_controller(request.cookies.get('cookies'))
        session_info =  [{'id':session['id'], 'start':session['start'],
                  'end':session['end'], 'status':session['status']}]
        return render_template('session_info.html', session_info= session_info)
    else:
        return redirect('/spots')


def get_spots_view():
    spots = get_available_spots_controller()
    if spots:
        return render_template('available_spots.html', spots= spots)
    else:
        return render_template('no_available_spots.html')
