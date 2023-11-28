from util.db import run_query
from sqlalchemy import select, insert, update, and_
from model.models import Product, ProductImage, Category

class ProductService:
    def __init__(self):
        pass

    def get_product_detail(self, product_id: str, is_admin: bool = False) -> list:
        query = select(
                    Product.id,
                    Product.product_name.label('title'),
                    Product.description.label('product_detail'),
                    Product.price,
                    Product.category_id,
                    Product.condition,
                    Category.category_name
                ).join(
                    Category, Category.id == Product.category_id
                ).where(
                    Product.id == product_id
                )

        if not is_admin:
            query = query.where(and_(Product.deleted_at == None))

        products = run_query(query)

        if not products:
            return 

        product_images = self.get_product_images(product_id)
        products[0]['size'] = ["S", "M", "L"]
        products[0]['images_url'] = [product_image['image'] for product_image in product_images]

        if not products[0]['images_url']:
            products[0]['images_url'].append("/image/default-product.png")

        return products[0]

    def add_product(self, product_data:dict):
        run_query(
            insert(
                Product
            ).values(
                product_data
            ), commit=True
        )
        
    def update_product(self, id_product:str, product_data:dict):
        run_query(
            update(
                Product
            ).values(
                product_data
            ).where(
                Product.id == id_product,
            ), commit=True
        )
    
    def get_products_by_category(self, category_id: str)->list:
        products = run_query(
            select(
                Product.id,
                Product.product_name.label('title'),
                Product.description.label('product_detail'),
                Product.price,
            )
            .where(
                Product.category_id == category_id,
                Product.deleted_at == None
            )
        )

        return products

    def get_product_images(self, product_id: str):
        images = run_query(
            select(
                ProductImage.image
            ).where(
                ProductImage.product_id == product_id,
                ProductImage.deleted_at == None
            )
        )

        return images
    
    def get_product_view(self, product_id: str, is_admin: bool = False):
        query = select(
                    Product.view
                ).where(
                    Product.id == product_id,
                )

        if not is_admin:
            query = query.where(and_(Product.deleted_at == None))

        products = run_query(query)

        return products[0]
    
    def update_product_view(self, product_id: str, view: int):
        run_query(
            update(
                Product
            ).values({
                'view': view
            }).where(
                Product.id == product_id
            ), commit=True
        )
