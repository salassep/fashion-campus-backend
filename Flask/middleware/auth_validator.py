from functools import wraps
from flask import request, abort
from jsonschema import validate, ValidationError

def validate_sign_up_payload(f):
    @wraps(f)
    def wrap_func(*args, **kwargs):
        sign_up_payload_schema = {
            "type": "object",
            "properties": {
                'name': { "type": "string" },
                'email': {
                    "type": "string",
                    "pattern": "^\S+@\S+\.\S+$",
                    "message": {
                        "pattern": "Email invalid"
                    }
                },
                'phone_number': { 
                    "type": "string",
                    "pattern": "^(^\+62|62|^08)(\d{3,4}-?){2}\d{3,4}$",
                    "message": {
                        "pattern": "Phone number invalid, must Indonesian phone number"
                    }
                },
                'password': {
                    "type": "string",
                    "pattern": "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$",
                    "message":{
                        "pattern": "password must have at least 8 character consisting of 1 uppercase, 1 lowercase, and 1 number"
                    }
                },
                'type': {
                    "type": "string",
                    "enum": ["buyer", "seller"]
                }
            },
            "required": ['name', 'email', 'phone_number', 'password'],
        }
        
        try:
            data = request.json
            validate(instance=data, schema=sign_up_payload_schema)
        except ValidationError as e:
            if e.validator == "pattern":
                abort(400, e.schema["message"]["pattern"])
            abort(400, e.message)
        
        return f(*args, **kwargs)
    
    return wrap_func

def validate_sign_in_payload(f):
    @wraps(f)
    def wrap_func(*args, **kwargs):
        sign_in_payload_schema = {
            "type": "object",
            "properties": {
                'name': { "type": "string" },
                'email': {
                    "type": "string",
                    "pattern": "^\S+@\S+\.\S+$",
                    "message": {
                        "pattern": "Email invalid"
                    }
                },
                'password': { "type": "string" },
            },
            "required": ['email', 'password'],
        }
        
        try:
            data = request.json
            validate(instance=data, schema=sign_in_payload_schema)
        except ValidationError as e:
            if e.validator == "pattern":
                abort(400, e.schema["message"]["pattern"])
            abort(400, e.message)
        
        return f(*args, **kwargs)
    
    return wrap_func