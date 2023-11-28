
from flask import Blueprint, request
from service.wishlist_service import WishlistService
from util.response import response
from middleware.token_validator import validate_token

wishlist_bp = Blueprint("wishlist", __name__, url_prefix="")

@wishlist_bp.route("/user/wishlist", methods=["GET"])
@validate_token
def wishlist(current_user):
    data = WishlistService().get_wishlist(current_user['user_id'])
    return response(200, data = data)


@wishlist_bp.route("/user/wishlist/<product_id>", methods=["POST","DELETE"])
@validate_token
def get_and_topup_balance(product_id, current_user):
    user_id = current_user['user_id']
    
    if request.method == "POST":
        WishlistService().add_wishlist({
            'user_id': user_id, 
            'product_id': product_id
        })
        return response(201, "Wishlist success Added")
    
    elif request.method == "DELETE":
        WishlistService().delete_wishlist(user_id, product_id)
        return response(200, "Wishlist success Deleted")
        
        
@wishlist_bp.route("/user/cek-wishlist", methods=["POST"])
@validate_token
def cek_wishlist(current_user):
    body = request.json
    product_id = body["product_id"]
    data = WishlistService().cek_wishlist(current_user['user_id'], product_id)
    
    if data:
        return response(200, custom=[("wishlist", True)])
    else:
        return response(200, custom=[("wishlist", False)])