
import uuid
from flask import Blueprint, request
from datetime import datetime
from service.admin_service import AdminService
from service.banner_service import BannerService
from service.image_service import ImageService
from middleware.token_validator import validate_token
from util.response import response

admin_banner_bp = Blueprint("admin_banner", __name__, url_prefix="")

@admin_banner_bp.route("/banners", methods=["POST"])
@validate_token
def add_banner(current_user):
    user_id = current_user['user_id']

    if not AdminService().is_admin(user_id): return response(403, msg="error : You are not admin")
    
    body = request.json
    title, image = body["title"], body["images"]
    
    image_name = ImageService().upload_image(image[0])
    BannerService().add_banner(
        {
            "id": uuid.uuid4(),
            "title": title,
            "image" : f"/image/{image_name}"
        })
        
    return response(201, "Banner success added")


@admin_banner_bp.route("/banners/<banner_id>", methods=["GET","PUT","DELETE"])
@validate_token
def get_edit_delete_banner(banner_id, current_user):
    user_id = current_user['user_id']
    if not AdminService().is_admin(user_id): return response(403, msg="error : You are not admin")
    
    if request.method == "GET":
        result = BannerService().get_banners_by_id(banner_id)
        return response(200, data=result[0])
        
    if request.method == "PUT":
        body = request.json
        title, image = body["title"], body["images"]
        
        image_name = ImageService().upload_image(image[0])
        BannerService().update_banner(banner_id,
            {
                "title": title,
                "image" : f"/image/{image_name}"
            })
        
        return response(200, "Banner success Updated")
    
    if request.method == "DELETE":
        BannerService().update_banner(banner_id, {
            "deleted_at": datetime.now()
        })
        
        return response(200, "Banner success Deleted")
    
    
@admin_banner_bp.route("/banners/restore/<banner_id>", methods=["PUT"])
@validate_token
def restore_banner(banner_id, current_user):
    user_id = current_user['user_id']
    if not AdminService().is_admin(user_id): return response(403, msg="error : You are not admin")
    
    if request.method == "PUT":
        BannerService().update_banner(banner_id, {
            "deleted_at": None
        })
        
        return response(200, "Banner success Restored")