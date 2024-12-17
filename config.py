import  os.path
from app.logs import logger


SECRET_KEY = 'pizda'
logger.debug('SECRET_KEY is set')
WORK_DIRECTORY = os.getcwd()
logger.debug('WORK_DIRECTORY is set')
TEMPLATES_PATH = WORK_DIRECTORY + '/templates'
