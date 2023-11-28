from functools import wraps
from flask import request, abort
from jsonschema import validate, ValidationError

def validate_post_cart_payload(f):
    @wraps(f)
    def wrap_func(*args, **kwargs):
        post_order_payload_schema = {
            "type": "object",
            "properties": {
                "shipping_method": { 
                    "type": "string",
                    "enum": ["next day", "regular"]
                },
                "shipping_address": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        'phone_number': { 
                            "type": "string",
                            "pattern": "^(^\+62|62|^08)(\d{3,4}-?){2}\d{3,4}$",
                            "message": {
                                "pattern": "Phone number invalid, must Indonesian phone number"
                            }
                        },
                        "address": {"type": "string"},
                        "city": {"type": "string"}
                    },
                    "required": ["name", "phone_number", "address", "city"]
                }
            },
            "required": ["shipping_method", "shipping_address"]
        }
        
        try:
            data = request.json
            validate(instance=data, schema=post_order_payload_schema)
        except ValidationError as e:
            if e.validator == "pattern":
                abort(400, e.schema["message"]["pattern"])
            abort(400, e.message)
        
        return f(*args, **kwargs)
    
    return wrap_func