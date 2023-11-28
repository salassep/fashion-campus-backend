"""
API Product List

[[Endpoint]]
- Method: GET
- URL: /products
- query parameter:
    - page: Integer (required)
    - page_size: Integer (required)
    - sort_by: String [required] -> "price a_z" , "price z-a"
    - category: String [optional]
    - price: String [optional] -> "price_termurah,price_termahal"
    - condition: String [optional]
    - product_name: String [optional]

[[Logic]]
- Menampilkan Products : Where deleted_at == NULL
- Menampilkan Products Join Categories: Where categories.deleted_at == NULL
- Menampilkan Product sesuai parameter yang diberikan

[[Endpoint]]
- Method: GET
- URL: /categories

[[Logic]]
- Menampilkan All Categories
"""

from flask import Blueprint, request, abort
from service.product_list_service import ProductListService
from service.category_service import CategoryService
from util.response import response
from service.admin_service import AdminService
from AI import main

product_list_bp = Blueprint("product_list", __name__, url_prefix="")
    
@product_list_bp.route("/products", methods=["GET"])
def product_list():
    argument = request.args
    token = request.headers.get("Authentication")
    category = argument.get("category")
    price = argument.get("price")
    condition = argument.get("condition")
    product_name = argument.get("product_name")
    sort_by = argument.get("sort_by")
    page = argument.get("page")
    page_size = argument.get("page_size")

    is_admin = False

    if token:
        is_admin = True if AdminService().is_admin(token) else False
    
    data = ProductListService().get_specific_product({
        'category': category, 
        'price': price, 
        'condition': condition, 
        'product_name': product_name, 
        'sort_by': sort_by,
        'page': page, 
        'page_size': page_size
    }, is_admin)
    
    return response(200, data=data["data"], custom=[("total_rows", data["total_rows"])])

@product_list_bp.route("/products/search_image", methods=["POST"])
def search_product_by_image():
    argument = request.json
    image = argument.get("image")

    category_result_by_image = main.input_image(image)

    result = CategoryService().get_category_by_name(category_result_by_image)

    if not result:
        abort(404, "Product not found")
    
    return result, 200

@product_list_bp.route("/categories", methods=["GET"])
def get_categories():
    token = request.headers.get("Authentication")

    is_admin = False

    if token: 
        is_admin = True if AdminService().is_admin(token) else False

    data = CategoryService().get_categories(is_use_image=False, is_admin=is_admin)
    return response(200, data = data)


@product_list_bp.route("/similar-product", methods=["GET"])
def get_similar_product():
    argument = request.args
    category_id = argument.get("category_id")
    product_id = argument.get("product_id")
    
    data = ProductListService().get_similar_product(category_id, product_id)
    return response(200, data = data)