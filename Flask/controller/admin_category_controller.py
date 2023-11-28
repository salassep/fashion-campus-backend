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

from datetime import datetime
from flask import Blueprint, request
from util.response import response
from service.admin_service import AdminService
from service.category_service import CategoryService
from middleware.token_validator import validate_token
import uuid

admin_category_bp = Blueprint("admin_category", __name__, url_prefix="")

"""
Menampilkan, Mengupdate, Menghapus Kategori
"""
@admin_category_bp.route("/categories", methods=["POST"])
@validate_token
def get_add_update_product(current_user):

    user_id = current_user['user_id']

    if not AdminService().is_admin(user_id): return response(403, msg="You are not admin")

    if request.method == "POST":
        body = request.json

        id_category = uuid.uuid4()
        CategoryService().add_category({
            'id': id_category,
            'category_name': body["category_name"]
        })

        return response(201, "Category success added")


"""
Menghapus Kategori
"""
@admin_category_bp.route("/categories/<id_category>", methods=["PUT","DELETE"])
@validate_token
def delete_product(id_category, current_user):
    user_id = current_user['user_id']

    if not AdminService().is_admin(user_id): return response(403, msg="You are not admin")
    
    if request.method == "PUT":
        body = request.json
        category_name = body["category_name"]

        CategoryService().update_category(
            id_category,
            {
                'category_name': category_name,
                'updated_at': datetime.now()
            }
        )

        return response(200, "Category success updated")
    
    if request.method == "DELETE":
        CategoryService().delete_category(
            id_category,{
                'deleted_at': datetime.now()
            }
        )

        return response(200, "Category success deleted")

"""
Menghapus Kategori
"""
@admin_category_bp.route("/categories/restore/<id_category>", methods=["POST"])
@validate_token
def restore_category(id_category, current_user):
    user_id = current_user['user_id']

    if not AdminService().is_admin(user_id): return response(403, msg="You are not admin")

    CategoryService().update_category(
        id_category,
        {
            'deleted_at': None
        }
    )

    return response(200, "Category success restored")
