"""
API sign up

[[Endpoint]]
- Method: POST
- URL: /sign-in
- Request body
    - email: string (required)
    - password: string (required)

[[Logic]]
- User mengirimkan semua data yang required
- Buat password menjadi MD5
"""
from flask import Blueprint, abort, request
from middleware.auth_validator import validate_sign_up_payload, validate_sign_in_payload
from service.auth_service import AuthService
from util.response import response

auth_bp = Blueprint("auth", __name__, url_prefix="")

@auth_bp.route("/sign-up", methods=["POST"])
@validate_sign_up_payload
def sign_up():
    try:
        body = request.json
        
        AuthService().sign_up(body)

        return response(201, msg="success, user created")

    except Exception as e:
        abort(400, str(e))
    
@auth_bp.route("/sign-in", methods=["POST"])
@validate_sign_in_payload
def sign_in():
    body = request.json
    result = AuthService().sign_in(body)

    if not result:
        abort(401, "Wrong credentials")
    
    return {
        "success": True,
        "user_information": {
            "name": result["name"],
            "email": result["email"],
            "phone_number": result["phone_number"],
            "type": result["type"]
        },
        "token": result["token"],
        "message": "Login success"
    }, 200
