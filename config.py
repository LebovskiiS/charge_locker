import os

SECRET_KEY = 'pizda'
WORK_DIRECTORY = os.getcwd()
TEMPLATES_PATH = os.path.join(WORK_DIRECTORY, 'templates')

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///" + os.path.join(WORK_DIRECTORY, 'charger_locker_database.db')