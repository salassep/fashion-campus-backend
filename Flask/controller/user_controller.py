"""
API sign up

[[Endpoint]]
- Method: GET
- URL: /user
- Request header
    - authentication : string (required)

[[Logic]]
- Cari User berdasarkan token / terjemahan token {"id_user": token}


[[Endpoint]]
- Method: POST
- URL: /user/shipping_address
- Request header
    - authentication : string (required)
- Request json
    - name : String (required)
    - phone_number : String (required)
    - address : String (required)
    - city : String (required)

[[Logic]]
- Cari User berdasarkan token / terjemahan token {"id_user": token}
- Menambahkan shipping_address sesuai input / request

[[Endpoint]]
- Method: GET || POST
- URL: /user/balance
- Request header
    - authentication : string (required)
- Request json (POST)
    - amount : Integer (required)

[[Logic]]
- Method GET : Menampilkan current balance
- Method POST : Menambah balance sesuai amount yang dikirim


[[Endpoint]]
- Method: GET
- URL: /user/order
- Request header
    - authentication : string (required)

[[Logic]]
- Mencari order sesuai user_id, mencari id order di table cart_order, 
- menghubungkan table cart_order dengan table cart dan 
- tampilkan produk yang akan di tampilkan pada cart

"""

from flask import Blueprint, request
from service.user_service import UserService
from util.response import response
from middleware.token_validator import validate_token

profile_bp = Blueprint("profile", __name__, url_prefix="")

"""
Menampilkan Detail Profile User
"""
@profile_bp.route("/user", methods=["GET"])
@validate_token
def profile(current_user):
    data = UserService().get_user(current_user['user_id'], 'buyer')[0]
    
    return response(200, data = data)


@profile_bp.route("/user/balance", methods=["GET","POST"])
@validate_token
def get_and_topup_balance(current_user):
    user_id = current_user['user_id']
    user_balance = UserService().get_user_balance(user_id)
    
    if request.method == "GET":
        return response(200, msg=f"Your balance : Rp {user_balance}", data={'balance': user_balance})
    
    elif request.method == "POST":
        amount = request.json["amount"]
        balance = UserService().get_user_balance(user_id) + amount
    
        UserService().update_user_balance(user_id, balance)
        
        return response(201, "Top Up balance success", custom=[('balance', balance)])