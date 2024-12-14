from datetime import datetime
from flask import request, render_template, redirect
from .controllers import (
    main_controller, submit_controller,
    get_session_by_token_controller, get_spot_info_by_id_controller,
    get_spot_info_by_token_controller, stop_booking_controller)
from . import db
from auth.jwt_token import create_token
from .decorators import check_token, delete_old_sessions
from app.logs import logger


def time_to_db_format(date_str: str, time_str: str) -> str:
    try:
        datetime_obj = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %I:%M %p')
        return datetime_obj.strftime('%Y-%m-%d %I:%M %p')
    except Exception as e:
        logger.error(f"Error parsing date/time: {e}")
        raise e


def full_time_to_12_hour_format(datetime_str: str) -> str:
    try:
        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        return datetime_obj.strftime('%I:%M %p')
    except Exception as e:
        logger.error(f"Error converting time to 12-hour format: {e}")
        raise e


def unix_to_12_hour_format(unix_timestamp: int) -> str:
    try:
        datetime_obj = datetime.fromtimestamp(unix_timestamp)  # Конвертируем UNIX timestamp в datetime
        return datetime_obj.strftime('%I:%M %p')  # Преобразуем в формат 12-часового времени (например, 04:30 PM)
    except Exception as e:
        logger.error(f"Error converting UNIX timestamp to 12-hour format: {e}")
        return "Invalid time"







@check_token
def main_view():
    logger.debug('main func started token found')
    session = main_controller(request.cookies.get('jwt'))  # Получаем данные сессии

    spot_id = session[1]
    start = session[2]  # UNIX timestamp
    end = session[3]  # UNIX timestamp

    # Преобразуем start и end в читаемый формат времени
    start = unix_to_12_hour_format(start)
    end = unix_to_12_hour_format(end)

    floor = session[6]
    building = session[7]
    spot_number = session[8]

    print(f'floor:{floor}, building:{building}, '
          f'spot_number:{spot_number}, start:{start}, end:{end}')
    logger.warning('main rendering session_info.html')

    return render_template(
        'session_info.html', spot_id=spot_id, start=start, end=end,
        floor=floor, building=building, spot_number=spot_number
    )






@delete_old_sessions
def get_spots_view():
    try:
        all_spots = db.get_all_spots()  # Данные из базы

        booked_spots = []
        available_spots = []

        for spot in all_spots:  # Разбиваем точки на группы
            if spot['end_time']:  # Если время окончания существует
                booked_spots.append(spot)
            else:  # Если доступен
                available_spots.append(spot)

        # Добавляем сортировку на основе времени окончания бронирования
        booked_spots.sort(key=lambda x: x['end_time'] if x['end_time'] else '')

        # Отображаем в удобном виде (например, группы по зданию)
        spots_grouped = {}
        for spot in available_spots:
            building = spot['building']
            floor = spot['floor']
            if building not in spots_grouped:
                spots_grouped[building] = {}
            if floor not in spots_grouped[building]:
                spots_grouped[building][floor] = {"available": []}
            spots_grouped[building][floor]["available"].append(spot)

        return render_template('spots.html', booked_spots=booked_spots, spots_grouped=spots_grouped)
    except Exception as e:
        logger.error(f"Error in get_spots_view: {e}")
        return f"Error: {e}"




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
    start_12_hour = request.form.get('time_start')  # Пример: "4:30 PM"
    end_12_hour = request.form.get('time_end')  # Пример: "6:00 PM"

    # Текущая дата для записи
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Форматируем время для записи в базу
    start_db_format = f"{current_date} {start_12_hour}"
    end_db_format = f"{current_date} {end_12_hour}"

    try:
        db.book_spot(token, spot_id, start_db_format, end_db_format)
        resp = redirect('/')
        resp.set_cookie(key='jwt', value=token, max_age=60 * 60 * 16)  # Примерно 16 часов
        return resp
    except Exception as e:
        logger.error(f"Error submitting view: {e}")
        return f"Something went wrong: {e}"



@check_token
def session_view():
    token = request.cookies.get('jwt')
    session_info = get_session_by_token_controller(token)  # id, spot_id, start, end, token
    spot_info = get_spot_info_by_token_controller(token)

    floor = spot_info[2]
    building = spot_info[3]
    spot_number = spot_info[4]
    start = session_info[5]  # UNIX timestamp
    end = session_info[6]  # UNIX timestamp

    # Приводим время в читаемый вид
    start = unix_to_12_hour_format(start)
    end = unix_to_12_hour_format(end)

    print(f'floor:{floor}, building:{building}, '
          f'spot_number:{spot_number}, start:{start}, end:{end}')
    return render_template(
        'session_info.html', start=start, end=end, floor=floor,
        building=building, spot_number=spot_number
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



def change_session_view():
    token = request.cookies.get('jwt')  # Извлекаем токен из cookie
    session = get_session_by_token_controller(token)  # Получаем текущую сессию
    spot_id = session[1]  # Извлекаем ID спота

    try:
        result = stop_booking_controller(token)
        if result != 'ok':
            raise Exception(f"Failed to stop booking for token {token}")
    except Exception as e:
        logger.error(f"Error while trying to stop booking: {e}")
        return render_template('error.html', message="Could not change session. Please try again.")

    # Переадресовываем на выбор времени
    return redirect(f'/time/{spot_id}')

