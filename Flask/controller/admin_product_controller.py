"""
API Admin Product

[[Endpoint]]
- Method: POST
- URL: /products
- Request header
    - authentication : string (required)
- Request json
    - product_name: string (required)
    - description: string (required)
    - images: list (required)
    - condition: string (required)
    - category_id: string (required)
    - price: integer (required)

[[Logic]]
- Cari User berdasarkan token / terjemahan token {"id_user": token}
- Menginput product sesuai parameter json
- Menginput image dari list parameter json images ke table product_images

[[Endpoint]]
- Method: PUT
- URL: /products
- Request header
    - authentication : string (required)
- Request json
    - id_product: string (required)
    - product_name: string (required)
    - description: string (required)
    - images: list (required)
    - condition: string (required)
    - category_id: string (required)
    - price: integer (required)

[[Logic]]
- Cari User berdasarkan token / terjemahan token {"id_user": token}
- Mengupdate product sesuai parameter json
- Menghapus image product sebelumnya
- Menginput image baru dari list parameter json images ke table product_images

[[Endpoint]]
- Method: DELETE
- URL: /products/<id_product>
- Request header
    - authentication : string (required)

[[Logic]]
- Cari User berdasarkan token / terjemahan token {"id_user": token}
- Menghapus product berdasarkan id product
- menghapus images berdasarkan id_product
"""

import uuid
from flask import Blueprint, request
from datetime import datetime
from service.admin_service import AdminService
from service.product_service import ProductService
from service.image_service import ImageService
from service.image_db_service import ImageDBService
from middleware.token_validator import validate_token
from middleware.product_validator import validate_post_product_payload, validate_put_product_payload
from util.response import response

admin_product_bp = Blueprint("admin_product", __name__, url_prefix="")

"""
- Menambah Product sekaligus menambah image ke table images
- Mengupdate Product, Menghapus product_images sebelumnya, dan menambah images baru
"""
@admin_product_bp.route("/products", methods=["POST"])
@validate_token
@validate_post_product_payload
def post_add_product(current_user):
    user_id = current_user['user_id']

    if not AdminService().is_admin(user_id): return response(403, msg="You are not admin")
    
    body = request.json
    product_name, description, images, condition, category_id, price = body["product_name"], body["description"], body["images"], body["condition"], body["category_id"], body["price"]
    
    id_product = uuid.uuid4()
    ProductService().add_product(
        {
            "id": id_product, 
            "product_name": product_name, 
            "description" : description, 
            "condition" : condition, 
            "category_id" : category_id, 
            "price" : price
        })
    
    if images:
        for image in images:
            image_name = ImageService().upload_image(image)
            ImageDBService().add_image(
                {
                    "id": uuid.uuid4(),
                    "image" : f"/image/{image_name}", 
                    "product_id" : id_product
                })
        
    return response(201, "Product success added")

@admin_product_bp.route("/products", methods=["PUT"])
@validate_token
@validate_put_product_payload
def put_update_product(current_user):
    user_id = current_user['user_id']

    if not AdminService().is_admin(user_id): return response(403, msg="You are not admin")
    
    body = request.json
    id_product, product_name, description, images, condition, category_id, price = body["product_id"], body["product_name"], body["description"], body["images"], body["condition"], body["category_id"], body["price"]

    ProductService().update_product(id_product,
        {
            "product_name": product_name, 
            "description" : description, 
            "condition" : condition, 
            "category_id" : category_id, 
            "price" : price, 
            "updated_at": datetime.now()
        })
    
    # Menghapus Image Lama
    ImageDBService().delete_image_product(id_product)
    # # Masukan Ulang Images Product
    if images:
        for image in images:
            image_name = ImageService().upload_image(image)
            ImageDBService().add_image(
                {
                    "id": uuid.uuid4(), 
                    "image" : f"/image/{image_name}", 
                    "product_id" : id_product
                })
        
    return response(201, "Product success updated")

"""
- Menghapus product
- Menghapus images
"""
@admin_product_bp.route("/products/<id_product>", methods=["DELETE"])
@validate_token
def delete_product(id_product, current_user):
    user_id = current_user['user_id']

    if not AdminService().is_admin(user_id): return response(403, msg="You are not admin")
    
    ProductService().update_product(id_product, {
        "deleted_at": datetime.now()
    })
    
    # ImageDBService().delete_image_product(id_product)
    
    return response(200, "Product success deleted")

"""
- Mengembalikan produk yang telah dihapus
"""
@admin_product_bp.route("/products/restore/<id_product>", methods=["POST"])
@validate_token
def restore_product(id_product, current_user):
    user_id = current_user['user_id']

    if not AdminService().is_admin(user_id): return response(403, msg="You are not admin")
    
    ProductService().update_product(id_product, {
        "deleted_at": None
    })
    
    return response(200, "Product success restore")
    