from functools import wraps
from flask import request, abort
from jsonschema import validate, ValidationError

def validate_post_cart_payload(f):
    @wraps(f)
    def wrap_func(*args, **kwargs):
        post_cart_payload_schema = {
            "type": "object",
            "properties": {
                'id': { "type": "string" },
                'quantity': { 
                    "type": "integer",
                    "minimum": 1
                },
                'size': {
                    "type": "string",
                    "enum": ["S", "M", "L"]
                }
            },
            "required": ['id', 'quantity', 'size']
        }
        
        try:
            data = request.json
            validate(instance=data, schema=post_cart_payload_schema)
        except ValidationError as e:
            abort(400, e.message)
        
        return f(*args, **kwargs)
    
    return wrap_func