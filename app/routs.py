from . import app
from .views import main_view, get_spots_view, choose_time_view, submit_view, session_view


app.add_url_rule('/', view_func= main_view, methods= ['GET'])


app.add_url_rule('/spots', view_func= get_spots_view, methods= ['GET'])


app.add_url_rule('/time/<spot_id>', view_func= choose_time_view, methods= ['GET'])


app.add_url_rule('/submit', view_func= submit_view, methods= ['POST'])


app.add_url_rule('/session', view_func= session_view, methods=['GET'], endpoint='session_view')