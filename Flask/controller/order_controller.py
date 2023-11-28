import uuid
from flask import Blueprint, request, abort
from service.product_service import ProductService
from service.shipping_service import ShippingService
from service.cart_service import CartService
from service.user_service import UserService
from service.order_service import OrderService
from util.response import response
from middleware.token_validator import validate_token
from middleware.order_validator import validate_post_cart_payload

order_bp = Blueprint("order", __name__, url_prefix="")

@order_bp.route("/order", methods=["POST"])
@validate_token
@validate_post_cart_payload
def create_order(current_user):

    if not CartService().is_cart_exists_by_user_or_cart_id(current_user['user_id']):
        abort(400, "Empty cart")

    balance = UserService().get_user_balance(current_user['user_id'])
    price = CartService().get_cart_total_price(current_user['user_id'])
    shipping_price = ShippingService().get_shipping_price(price, request.json['shipping_method'])
    total_price = price + shipping_price
    
    if balance < total_price:
        abort(400, "Need top up")

    request.json['shipping_address']['user_id'] = current_user['user_id']
    ShippingService().add_shipping_address(request.json['shipping_address'])

    order_id = uuid.uuid4()
    shipping_address_id = ShippingService().get_shipping_address(current_user['user_id'])['id']
    shipping_option_id = ShippingService().get_shipping_option_id(request.json['shipping_method'])

    OrderService().create_order({
        'id': order_id,
        'shipping_address_id': shipping_address_id,
        'shipping_option_id': shipping_option_id,
        'user_id': current_user['user_id'],
        'status': 'Waiting',
        'total_order': total_price
    })
    
    CartService().checkout_cart(current_user['user_id'])
    UserService().update_user_balance(current_user['user_id'], balance-total_price)

    return response(201, "Order success")


@order_bp.route("/user/order", methods=["GET"])
@validate_token
def get_orders(current_user):
    result = OrderService().get_orders(current_user['user_id'])
    
    mapped_result = []

    for value in result:
        shipping_method = ShippingService().get_shipping_option_by_id(value['shipping_option_id'])
        shipping_address = ShippingService().get_shipping_address_by_id(value['shipping_address_id'])
        products = []
        for product in value["products"]:
            images = ProductService().get_product_images(product['product_id'])
            products.append({
                'id': product['product_id'],
                'details': {
                    'quantity': product['quantity'],
                    'size': product['size']
                },
                'price': product['price'] * product["quantity"],
                'name': product['product_name'],
                'image': images[0]['image'] if images else '/image/default-product.png'
            })

        del shipping_address["id"]
        
        mapped_result.append({
            "id": value["id"],
            "created_at": f'{value["created_at"]:%a, %d %B %Y}',
            "products": products,
            "shipping_method": shipping_method["name"],
            "status": value["status"],
            "shipping_address": shipping_address
        })
    
    return response(200, data=mapped_result)


@order_bp.route("/order/status/<status>/<order_id>", methods=["PUT"])
@validate_token
def update_order(status, order_id, current_user):
    if status == "arrive": status_change = "Arrived"
    else : status_change = "Waiting"
    
    OrderService().update_status_order({
        'id': order_id,
        'status': status_change
    })
    
    return response(200, f"Status success di update : {status_change}") 