from util.db import run_query
from sqlalchemy import select, func, desc, and_
from model.models import Product, Category, ProductImage
import math

class ProductListService:
    def __init__(self):
        pass
    
    def get_specific_product(self, filter_product_data: dict, is_admin: bool = False):
        category = filter_product_data['category']
        price = filter_product_data['price']
        condition = filter_product_data['condition']
        product_name = filter_product_data['product_name']
        sort_by = filter_product_data['sort_by']
        page = filter_product_data['page'] if filter_product_data['page'] else 1
        page_size = filter_product_data['page_size'] if filter_product_data['page_size'] else 10
                
        query = select(
                [Product.id,
                func.min(ProductImage.image).label('image'),
                Product.product_name.label('title'),
                Product.price,
                Product.category_id,
                Product.condition,
                Product.deleted_at,
                Category.deleted_at.label('category_deleted_at')]
            ).join(
                Category, Product.category_id == Category.id
            ).join(
                ProductImage, ProductImage.product_id == Product.id, isouter=True
            ).order_by(
                desc(Product.created_at)
            ).group_by(
                Product.id,
                Category.deleted_at
            )
        
        if not is_admin:
            query = query.filter(
                Product.deleted_at == None,
                Category.deleted_at == None
            )

        if category:
            categories_id = category.split(',')
            query = query.filter(
                and_(Product.category_id.in_(categories_id))
            )
                
        if price:
            filter_price = price.split(',') 
            query = query.filter(and_(Product.price.between(filter_price[0], filter_price[1])))
            
        if condition:
            condition_id = condition.split(',')
            query = query.filter(
                and_(Product.condition.in_(condition_id))
            )
                
        if  product_name:
            query = query.filter(and_(Product.product_name.like(f'%{product_name}%')))
            
        if sort_by: 
            sort = sort_by.lower()
            if sort == "price a_z":
                query = query.order_by(Product.price)
            elif sort == "price z_a":
                query = query.order_by(desc(Product.price))
                
        try:
            page = int(page)
            page_size = int(page_size)
        except ValueError:
            page = 1
            page_size = 10

        try:
            data = run_query(query)
            
            if len(data) < page_size or is_admin: 
                page_size = len(data)
                total_page = 1
                
            if len(data) > page_size : 
                total_page = math.ceil(len(data) / page_size)

            data_send = [data[i:i+page_size] for i in range(0, len(data), page_size)][page-1]
            
            for index, value in enumerate(data_send):
                data_send[index]["category_deleted"] = True if data_send[index]["category_deleted_at"] else False
                del data_send[index]["category_deleted_at"]
                del data_send[index]["category_id"]
                del data_send[index]["condition"]
                if not data_send[index]["image"]:
                    data_send[index]["image"] = "/image/default-product.png"
                    
            data_return = {
                "data":data_send, 
                "total_rows": len(data)
            }
        except:
            data_return = {
                "data": [],
                "total_rows": 0
            }

        return data_return
    
    def get_similar_product(self, category_id:str, product_id:str):
        query = select(
                [Product.id,
                func.min(ProductImage.image).label('image'),
                Product.product_name.label('title'),
                Product.price]
            ).join(
                ProductImage, ProductImage.product_id == Product.id, isouter=True
            ).filter(
                Product.deleted_at == None,
                Product.category_id == category_id,
                Product.id != product_id
            ).group_by(
                Product.id
            )
        
        data = run_query(query)
        if len(data) > 6:
            data = data[0:6]
            
        return data
    
    def get_popular_product(self):
        query = select(
                [Product.id,
                func.min(ProductImage.image).label('image'),
                Product.product_name.label('title'),
                Product.price]
            ).join(
                ProductImage, ProductImage.product_id == Product.id, isouter=True
            ).filter(
                Product.deleted_at == None
            ).group_by(
                Product.id
            ).order_by(desc(Product.view))
        
        data = run_query(query)
        if len(data) > 4:
            data = data[0:4]
            
        return data