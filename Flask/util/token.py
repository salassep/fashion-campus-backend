import jwt
import os
from datetime import datetime, timedelta

def generate_token(payload: dict) -> str:
    exp_time = datetime.now() + timedelta(minutes=int(os.environ["JWT_EXPIRATION_TIME_IN_MINUTES"]))
    payload['exp'] = exp_time
    return jwt.encode(payload, os.environ["JWT_TOKEN_KEY"], algorithm='HS256')

def verify_token(token: str) -> dict:
    try:    
        decode_token = jwt.decode(token, os.environ["JWT_TOKEN_KEY"], algorithms=['HS256'])
        return decode_token
    
    except jwt.ExpiredSignatureError:
        raise Exception("Token is expired")
    except jwt.InvalidTokenError:
        raise Exception("Token invalid")
