from . import app
from .views import (main_view, get_spots_view, info_view_en,
                    choose_time_view, submit_view, info_view_ch,
                    session_view, info_view_fa,
                    info_view_ru, stop_booking_view, change_session_view)


app.add_url_rule('/', view_func= main_view, methods= ['GET'])


app.add_url_rule('/spots', view_func= get_spots_view, methods= ['GET'])


app.add_url_rule('/time/<spot_id>', view_func= choose_time_view, methods= ['GET'])


app.add_url_rule('/submit', view_func= submit_view, methods= ['POST'])


app.add_url_rule('/session', view_func= session_view, methods=['GET'], endpoint='session_view')


app.add_url_rule('/stop', view_func= stop_booking_view, methods= ['GET'])

app.add_url_rule('/session/change', view_func= change_session_view, methods=['GET'])

app.add_url_rule('/info/en', view_func= info_view_en, methods=['GET'])
app.add_url_rule('/info/ch', view_func= info_view_ch, methods=["GET"])
app.add_url_rule('/info/ru', view_func= info_view_ru, methods=["GET"])
app.add_url_rule('/info/fa', view_func= info_view_fa, methods=["GET"])