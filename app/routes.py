from . import app
from .views import main_view, select_time, success_page, failure_page, spots_add_view



app.add_url_rule('/main', view_func= main_view, methods=['GET'])
app.add_url_rule('/book/<int:spot_id>/time', view_func=select_time, methods=['GET', 'POST'])
app.add_url_rule('/success', view_func= success_page, methods=['GET'])
app.add_url_rule('/failure', view_func= failure_page, methods=['GET'])
app.add_url_rule('/spots/add', view_func= spots_add_view, methods=['GET'] )
