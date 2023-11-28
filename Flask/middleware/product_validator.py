from functools import wraps
from flask import request, abort
from jsonschema import validate, ValidationError

def validate_post_product_payload(f):
    @wraps(f)
    def wrap_func(*args, **kwargs):
        post_shipping_address_payload_schema = {
            "type": "object",
            "properties": {
                'product_name': { "type": "string" },
                'description': { "type": "string" },
                'images': { "type": "array" },
                'condition': {
                    "type": "string",
                    "enum": ["used", "new"]
                },
                'category_id': { "type": "string" },
                'price': { 
                    "type": "integer",
                    "minimum": 0
                }
            },
            "required": ['product_name', 'description', 'images', 'condition', 'category_id', 'price']
        }
        
        try:
            data = request.json
            validate(instance=data, schema=post_shipping_address_payload_schema)

            allowed_formats = ["image"]

            for image in data["images"]:
                splitted_base64_image = image.split('base64')

                if "image" not in splitted_base64_image[0]:
                    raise Exception("The file not an image")

                base64_image = splitted_base64_image[1]

                file_size_estimate = len(base64_image) * 3 / 4 - base64_image.count('=', -2)
                if file_size_estimate >= 500000:
                    raise Exception("File is too big (500kb max)")
                
        except ValidationError as e:
            abort(400, e.message)
        
        except Exception as e:
            abort(400, str(e))
        
        return f(*args, **kwargs)
    
    return wrap_func

def validate_put_product_payload(f):
    @wraps(f)
    def wrap_func(*args, **kwargs):
        put_product_payload_schema = {
            "type": "object",
            "properties": {
                'id_product': { "type": "string" },
                'product_name': { "type": "string" },
                'description': { "type": "string" },
                'images': { "type": "array" },
                'condition': {
                    "type": "string",
                    "enum": ["used", "new"]
                },
                'category_id': { "type": "string" },
                'price': { 
                    "type": "integer",
                    "minimum": 0
                }
            },
            "required": ['product_name', 'description', 'images', 'condition', 'category_id', 'price']
        }
        
        try:
            data = request.json
            validate(instance=data, schema=put_product_payload_schema)

            for image in data["images"]:
                
                if "base64" not in image:
                    continue

                splitted_base64_image = image.split('base64')

                if "image" not in splitted_base64_image[0]:
                    raise Exception("The file not an image")

                base64_image = splitted_base64_image[1]

                file_size_estimate = len(base64_image) * 3 / 4 - base64_image.count('=', -2)
                if file_size_estimate >= 500000:
                    raise Exception("File is too big (500kb max)")
                
        except ValidationError as e:
            abort(400, e.message)
        
        except Exception as e:
            abort(400, str(e))
        
        return f(*args, **kwargs)
    
    return wrap_func