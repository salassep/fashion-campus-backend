import uuid

from datetime import datetime
from util.db import run_query
from sqlalchemy import select, delete, insert, func
from model.models import Wishlist, Product, ProductImage

class WishlistService:
    def __init__(self):
        pass
    
    def get_wishlist(self, user_id: str):
        return run_query(
            select(
                Wishlist.product_id,
                Product.product_name,
                Product.price,
                func.min(ProductImage.image).label('image'),
            ).join(
                Product, Wishlist.product_id == Product.id, isouter=True
            ).join(
                ProductImage, ProductImage.product_id == Product.id, isouter=True
            ).where(
                Product.deleted_at == None,
                Wishlist.user_id == user_id
            ).group_by(
                Wishlist.product_id,
                Product.product_name,
                Product.price
            )
        )
        
    def cek_wishlist(self, user_id: str, product_id:str):
        return run_query(
            select(
                Wishlist.product_id,
            ).where(
                Wishlist.user_id == user_id,
                Wishlist.product_id == product_id
            )
        )
    
    def add_wishlist(self, wishlist_data:dict):
        wishlist_data["id"] = uuid.uuid4()
        run_query(
            insert(
                Wishlist
            ).values(
                wishlist_data
            ), commit=True
        )
        
    def delete_wishlist(self, user_id: str, product_id: str):
        run_query(
            delete(
                Wishlist
            ).where(
                Wishlist.user_id == user_id,
                Wishlist.product_id == product_id
            ), commit=True
        )