from datetime import datetime
from util.db import run_query
from sqlalchemy import select, update
from model.models import User

class UserService:
    def __init__(self):
        pass
    
    def get_user(self, user_id: str, type: str):
        return run_query(
            select(
                User.name,
                User.email,
                User.phone_number
            ).where(
                User.id == user_id,
                User.type == type,
                User.deleted_at == None,
            )
        )
        
    def get_user_balance(self, user_id: str) -> int:
        balance = run_query(
            select(
                User.balance
            ).where(
                User.id == user_id,
                User.deleted_at == None,
            )
        )

        return balance[0]['balance']

    def update_user_balance(self, user_id: str, balance: int):
        run_query(
            update(
                User
            ).values({
                'balance': balance
            }).where(
                User.id == user_id,
                User.deleted_at == None,
            ), commit=True
        )
