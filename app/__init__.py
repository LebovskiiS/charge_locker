from flask import Flask
from config import TEMPLATES_PATH

app = Flask(__name__, template_folder= TEMPLATES_PATH)

from data_base.db import Database

db = Database()
from . import routs

@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    if date is None:
        return ''
    if fmt is None:
        fmt = '%I:%M%p'  # Default format
    return date.strftime(fmt)

print('return from delete old sessions', db.delete_old_sessions())

