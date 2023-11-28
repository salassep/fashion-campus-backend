from util.db import run_query
from sqlalchemy import select, insert, update, and_
from model.models import Banner

class BannerService:
    def __init__(self):
        pass

    def get_banners(self, is_admin: bool = False) -> list:
        query = select(
                    Banner.id,
                    Banner.image,
                    Banner.title,
                    Banner.deleted_at
                )
        
        if not is_admin:
            query = query.where(and_(Banner.deleted_at == None))
            
        banners = run_query(query)
        
        return banners
    
    def get_banners_by_id(self, banner_id:str) -> list:
        query = select(
                    Banner.id,
                    Banner.image,
                    Banner.title
                ).where(
                    Banner.id == banner_id,
                )
            
        banners = run_query(query)
        
        return banners
    
    def add_banner(self, banner_data:dict):
        run_query(
            insert(
                Banner
            ).values(
                banner_data
            ), commit=True
        )
    
    def update_banner(self, banner_id: str, banner_data:dict):
        run_query(
            update(
                Banner
            ).values(
                banner_data
            ).where(
                Banner.id == banner_id,
            ), commit=True
        )