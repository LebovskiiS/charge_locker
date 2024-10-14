from flask import Flask
from config import TEMPLATES_PATH

app = Flask(__name__, template_folder= TEMPLATES_PATH)

from data_base.db import Database

db = Database()
from . import routs

