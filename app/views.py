from flask import render_template, request, redirect, url_for
from .controllers import get_spots, book_spot_with_time
from .exceptions.exceptions import ExceptionSlotIsntAvailable


def main_view():
    spots = get_spots()
    print(spots)
    return render_template('main.html', spots= spots)


def select_time(spot_id):
    if request.method == 'POST':
        selected_time = request.form['time']
        try:
            result = book_spot_with_time(spot_id, selected_time)
            return redirect(url_for('success_page'))
        except ExceptionSlotIsntAvailable:
            return redirect(url_for('failure_page'))
    return render_template('select_time.html', spot_id=spot_id)


def success_page():
    return "Booking successful!"


def failure_page():
    return "Booking failed. Spot is not available."


def spots_add_view():
    return render_template('add_spots.html')