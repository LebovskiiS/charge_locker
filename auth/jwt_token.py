
import jwt
import datetime
from config import SECRET_KEY


def create_token():
    token = jwt.encode(payload={'datetime': datetime.datetime.now().isoformat()}, key= SECRET_KEY, algorithm= 'HS256')
    return token

def decode_token(token):
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    return decoded_token
