from app import app
from app.logs import logger

if __name__ == '__main__':
    logger.warning('the app started')
    app.run(debug= True, port= 5432, host= '0.0.0.0')

