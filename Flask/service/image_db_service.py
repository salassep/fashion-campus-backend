from util.db import run_query
from sqlalchemy import select, insert, update, delete
from model.models import ProductImage

class ImageDBService:
    def _init__(self):
        pass

    def add_image(self, image_data:dict):
        run_query(
            insert(
                ProductImage
            ).values(
                image_data
            ), commit=True
        )
        
    def delete_image_product(self, product_id: str):
        run_query(
            delete(
                ProductImage
            ).where(
                ProductImage.product_id == product_id
            ), commit=True
        )