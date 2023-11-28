from datetime import datetime
from util.db import run_query
from sqlalchemy import select, func, or_
from model.models import User , Order

class AdminService:
    def __init__(self):
        pass
    
    def is_admin(self, user_id: str):
        return run_query(
            select(
                User.name
            ).where(
                or_(User.id == user_id, User.token == user_id),
                User.type == 'seller',
                User.deleted_at == None,
            )
        )
        
    def get_sales(self):
        sales = run_query(select(func.sum(Order.total_order).label("total_sales")))
        
        return sales[0]['total_sales']