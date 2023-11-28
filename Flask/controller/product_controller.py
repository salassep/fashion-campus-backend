from flask import Blueprint, abort, request
from service.product_service import ProductService
from service.admin_service import AdminService
from util.response import response

product_detail_bp = Blueprint("product_detail", __name__, url_prefix="/products")

@product_detail_bp.route("/<id>", methods=["GET"])
def get_detail_product(id):
    token = request.headers.get("Authentication")

    is_admin = False

    if token: 
        is_admin = True if AdminService().is_admin(token) else False

    curr_view = ProductService().get_product_view(id, is_admin)
    ProductService().update_product_view(id, curr_view["view"] + 1)
        
    result = ProductService().get_product_detail(id, is_admin)

    if not result:
        abort(404, 'Product not found')

    return response(200, data = result)