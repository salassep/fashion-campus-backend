from functools import wraps
from flask import request, abort
from jsonschema import validate, ValidationError

def validate_post_shipping_address_payload(f):
    @wraps(f)
    def wrap_func(*args, **kwargs):
        post_shipping_address_payload_schema = {
            "type": "object",
            "properties": {
                'name': { "type": "string" },
                'phone_number': { "type": "string" },
                'address': { "type": "string" },
                'city': { "type": "string" }
            },
            "required": ['name', 'phone_number', 'address', 'city']
        }
        
        try:
            data = request.json
            validate(instance=data, schema=post_shipping_address_payload_schema)
        except ValidationError as e:
            abort(400, e.message)
        
        return f(*args, **kwargs)
    
    return wrap_func