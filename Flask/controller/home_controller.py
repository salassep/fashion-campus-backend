from flask import Blueprint, request
from service.banner_service import BannerService
from service.category_service import CategoryService
from service.product_list_service import ProductListService
from service.admin_service import AdminService
from util.response import response
import random

home_bp = Blueprint("home", __name__, url_prefix="/home")

@home_bp.route("/banner", methods=["GET"])
def get_banners():
    token = request.headers.get("Authentication")

    is_admin = False

    if token: 
        is_admin = True if AdminService().is_admin(token) else False
        
    result = BannerService().get_banners(is_admin)
    return response(200, data=result)

@home_bp.route("/nav/category", methods=["GET"])
def get_nav_categories():
    result = CategoryService().get_categories()
    # random.shuffle(result)

    return response(200, data=result[0:4])

@home_bp.route("/category", methods=["GET"])
def get_categories():
    result = CategoryService().get_categories()
    random.shuffle(result)

    return response(200, data=result[0:6])

@home_bp.route("/popular-product", methods=["GET"])
def get_popular_product():
    result = ProductListService().get_popular_product()

    return response(200, data=result)