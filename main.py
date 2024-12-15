from app import app
from app.logs import logger

if __name__ == '__main__':
    logger.warning('the app started')
    app.run(debug= True, port= 4000, host= '0.0.0.0')

