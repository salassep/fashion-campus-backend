import uuid
from flask import Blueprint, abort, request
from service.cart_service import CartService
from service.product_service import ProductService
from util.response import response
from middleware.token_validator import validate_token
from middleware.cart_validator import validate_post_cart_payload

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")

@cart_bp.route("", methods=["POST"])
@validate_token
@validate_post_cart_payload
def add_to_cart(current_user):
    try:
        id_cart = uuid.uuid4()
        CartService().add_to_cart({
            'id': id_cart,
            'user_id': current_user['user_id'],
            'product_id': request.json['id'],
            'quantity': request.json['quantity'],
            'size': request.json['size']
        })

        return response(201, 'success added item to cart')
    
    except Exception as e:
        abort(404, str(e))

@cart_bp.route("", methods=["GET"])
@validate_token
def get_user_cart(current_user):
    result = CartService().get_user_carts(current_user['user_id'])

    mapped_result = []

    for value in result:
        images = ProductService().get_product_images(value['product_id'])
        mapped_result.append({
            'id': value['id'],
            'details': {
                'quantity': value['quantity'],
                'size': value['size']
            },
            'price': value['price'],
            'name': value['product_name'],
            'image': images[0]['image'] if images else '/image/default-product.png'
        })

    return response(200, data = mapped_result)

@cart_bp.route("<cart_id>", methods=["DELETE"])
def delete_cart_item(cart_id):
    if not CartService().is_cart_exists_by_user_or_cart_id(cart_id):
        abort(404, "Cart not found")

    CartService().delete_cart(cart_id)

    return response(200, "Cart success deleted")
