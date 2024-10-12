from flask import Flask


app = Flask(__name__)
from data_base.db import Database
db = Database()