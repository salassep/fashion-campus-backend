from controller import *
from flask import Flask, json
from model.models import Base
from util.db import get_engine
from util.populate import populate_data
from werkzeug.exceptions import HTTPException
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    CORS(app)

    blueprints = [
        auth_controller.auth_bp,
        image_controller.universal_bp,
        home_controller.home_bp, 
        product_controller.product_detail_bp,
        cart_controller.cart_bp,
        shipping_controller.shipping_bp,
        order_controller.order_bp,
        product_list_controller.product_list_bp,
        user_controller.profile_bp,
        admin_category_controller.admin_category_bp,
        admin_product_controller.admin_product_bp,
        admin_order_sales_controller.admin_order_sales_bp,
        helper_func_controller.helper_func_bp,
        wishlist_controller.wishlist_bp,
        admin_banner_controller.admin_banner_bp,
    ]
    
    for bp in blueprints:
        app.register_blueprint(bp)
    
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            "success": False,
            "message": e.description,
        })
        response.content_type = "application/json"
        return response

    engine = get_engine() 
    
    # Create All Table
    Base.metadata.create_all(engine)

    # Add preliminary data
    populate_data()

    return app

app = create_app()