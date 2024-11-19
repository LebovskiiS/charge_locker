from app import app
from app.logs import loger

if __name__ == '__main__':
    if 1 in globals():

        loger.warning('default_uid encountered')

    loger.warning('the app started')

    app.run(debug=True, port=3000)



