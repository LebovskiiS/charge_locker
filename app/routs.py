from . import app
from .views import main_view, get_spots_view

app.add_url_rule('/', view_func= main_view, methods= ['GET'])

app.add_url_rule('/spots', view_func= views.get_spots_view, methods= ['GET', 'POST'])

app.add_url_rule('/book_spot', view)