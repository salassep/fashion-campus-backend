from util.db import run_query
from sqlalchemy import select, insert, update
from model.models import Category, Product, ProductImage

class CategoryService:
    def _init__(self):
        pass

    def get_categories(self, is_use_image: str = True, is_admin = False) -> list:
        query = select(
            Category.id,
            Category.category_name.label('title'),
            Category.deleted_at,
        )

        if not is_admin:
            query = query.where(Category.deleted_at == None)

        categories = run_query(query)

        if is_use_image:
            for index, value in enumerate(categories):
                categories[index]['image'] = self.get_category_image(value['id'])

        return categories
    
    def get_category_by_name(self, category_name):
        categories = run_query(
            select(
                Category.id.label('category_id')
            ).where(
                Category.category_name == category_name,
                Category.deleted_at == None,
            )
        )

        if not categories:
            return
        
        return categories[0]
    
    def get_category_image(self, category_id: str) -> str:
        image = run_query(
            select(
                ProductImage.image
            ).join(
                Product, ProductImage.product_id == Product.id
            ).filter(
                Product.category_id == category_id
            ).limit(1)
        )

        if not image:
            return '/image/default.png'

        return image[0]['image']

    def add_category(self, category_data:dict):
        run_query(
            insert(
                Category
            ).values(
                category_data
            ), commit=True
        )
        
    def update_category(self, id_category:str, category_data:dict):
        run_query(
            update(
                Category
            ).values(
                category_data
            ).where(
                Category.id == id_category
            ), commit=True
        )
        
    def delete_category(self, id_category: str, category_data: dict):
        run_query(
            update(
                Category
            ).values(
                category_data
            ).where(
                Category.id == id_category,
                Category.deleted_at == None
            ), commit=True
        )
