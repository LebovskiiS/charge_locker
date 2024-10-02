from flask import  Flask
from .database.db import Database


app = Flask(__name__)
db = Database()

