from functools import wraps
from flask import abort, request
from util.token import verify_token

def validate_token(f):  
    @wraps(f)
    def wrap_func(*args, **kwargs):
        token = request.headers.get('Authentication')

        if not token:
            abort(401, "Token is required")
        
        try:
            data = verify_token(token)
        except Exception as e:
            abort(401, str(e))
        
        return f(current_user=data, *args, **kwargs)
    
    return wrap_func
