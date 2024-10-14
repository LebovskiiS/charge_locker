from . import app
from .views import main_view, get_spots_view, book_time_view, submit_view

app.add_url_rule('/', view_func= main_view, methods= ['GET'])

app.add_url_rule('/spots', view_func= get_spots_view, methods= ['GET'])

app.add_url_rule('/book_spot', view_func= book_time_view, methods= ['GET'])
app.add_url_rule('/submit', view_func= submit_view, methods= ['POST'] )