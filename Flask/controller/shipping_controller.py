from flask import Blueprint, abort, request
from service.shipping_service import ShippingService
from service.cart_service import CartService
from middleware.token_validator import validate_token
from middleware.shipping_address_validator import validate_post_shipping_address_payload
from util.response import response
import uuid

shipping_bp = Blueprint("shipping", __name__, url_prefix="")

@shipping_bp.route("/user/shipping_address", methods=["GET"])
@validate_token
def get_user_address(current_user):
    result = ShippingService().get_shipping_address(current_user["user_id"])
    return response(200, data = result)

@shipping_bp.route("/user/shipping_address", methods=["POST"])
@validate_token
@validate_post_shipping_address_payload
def post_user_address(current_user):
    body = request.json
    ShippingService().add_shipping_address({
        "id": uuid.uuid4(),
        "user_id":current_user["user_id"],
        "name": body["name"], 
        "phone_number": body["phone_number"],
        "address": body["address"], 
        "city": body["city"]
    })
    
    return response(201, "shipping address success changed", data=body)


@shipping_bp.route("/shipping_price", methods=["GET"])
@validate_token
def get_shipping_price(current_user):
    total_price = CartService().get_cart_total_price(current_user['user_id'])
        
    if not total_price:
        abort(400, "Cart empty")

    result = ShippingService().get_shipping_price(total_price)

    return response(200, data = result)
