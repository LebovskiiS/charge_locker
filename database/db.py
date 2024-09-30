import sqlite3
from .scripts import spots_db, sessions_db, users_db

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('data_base.db', check_same_thread= False)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute(spots_db)
        self.cursor.execute(sessions_db)
        self.cursor.execute(users_db)


    def
