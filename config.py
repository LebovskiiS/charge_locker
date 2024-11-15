import  os.path
from dotenv import load_dotenv
load_dotenv()
import os

HOME_DIRRECTORY = os.path.expanduser('~')

SECRET_KEY_FILE = os.path.join(HOME_DIRRECTORY + '/Desktop/SECRET_KEY')


DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOSTNAME = os.getenv('DB_HOSTNAME')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')




SECRET_KEY = 'pizda'
WORK_DIRECTORY = os.getcwd()
TEMPLATES_PATH = WORK_DIRECTORY + '/templates'
