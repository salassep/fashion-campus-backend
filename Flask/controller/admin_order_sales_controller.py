"""
API Admin Categories

[[Endpoint]]
- Method: POST
- URL: /categories
- Request header
    - authentication : string (required)
- Request json
    - category_name: String (required)

[[Logic]]
- Cari User berdasarkan token / terjemahan token {"id_user": token}
- Menambah Categori

[[Endpoint]]
- Method: PUT
- URL: /categories
- Request header
    - authentication : string (required)
- Request json
    - id_category: String (required)
    - category_name: String (required)

[[Logic]]
- Cari User berdasarkan token / terjemahan token {"id_user": token}
- Mengupdate Categori

[[Endpoint]]
- Method: Delete
- URL: /categories/<id_category>
- Request header
    - authentication : string (required)

[[Logic]]
- Cari User berdasarkan token / terjemahan token {"id_user": token}
- Menghapus Categori sesuai id pada route url

"""

from flask import Blueprint, request
from util.response import response
from service.admin_service import AdminService
from service.order_service import OrderService
from service.product_service import ProductService
from middleware.token_validator import validate_token

admin_order_sales_bp = Blueprint("admin_order_sales", __name__, url_prefix="")

@admin_order_sales_bp.route("/orders", methods=["GET"])
@validate_token
def get_orders(current_user):
    user_id = current_user['user_id']

    if not AdminService().is_admin(user_id): return response(403, msg="You are not admin")

    argument = request.args
    sort_by = argument.get("sort_by")
    page = argument.get("page")
    page_size = argument.get("page_size")
    
    result = OrderService().get_admin_orders({
        'sort_by': sort_by,
        'page': page,
        'page_size': page_size
    })

    mapped_result = []

    for value in result:
        mapped_result.append({
            "id": value['id'],
            "created_at": f'{value["created_at"]:%a, %d %B %Y}',
            "user_email": value['email'],
            "user_name": value["name"],
            "user_id": value['user_id'],
            "total": value['total_order'],
            "status": value['status']
        })
        
    return response(200, data = mapped_result)

@admin_order_sales_bp.route("/orders/status/<status>/<order_id>", methods=["PUT"])
@validate_token 
def update_orders(status, order_id, current_user):
    user_id = current_user['user_id']

    if not AdminService().is_admin(user_id): return response(403, msg="You are not admin")
    
    if status == "process": status_change = "Processed"
    elif status == "deliver": status_change = "Delivered"
    else : status_change = "Waiting"
    
    OrderService().update_status_order({
        'id': order_id,
        'status': status_change
    })
    
    return response(200, f"Status success di update : {status_change}")

@admin_order_sales_bp.route("/sales", methods=["GET"])
@validate_token
def get_sales(current_user):
    user_id = current_user['user_id']

    if not AdminService().is_admin(user_id): return response(403, msg="You are not admin")
    
    sales = AdminService().get_sales() if AdminService().get_sales() else 0

    return response(200, data={'total': sales})