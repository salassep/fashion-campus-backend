import hashlib
import uuid
from model.models import User
from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError
from util.db import run_query
from util.token import generate_token

class AuthService:
    def __init__(self):
        pass

    def sign_up(self, data: dict):
        try:
            data["id"] = uuid.uuid4()
            data["password"] = hashlib.md5(data["password"].encode()).hexdigest()
            if "type" not in data:
                data["type"] = "buyer"

            run_query(
                insert(
                    User
                ).values(
                    data
                ), commit=True
            )

            return data
        except IntegrityError:
            # case: when user already exists
            raise Exception("User with the same name / email / phone already exists")
    
    def sign_in(self, data: dict):
        data["password"] = hashlib.md5(data["password"].encode()).hexdigest()
        users = run_query(
            select(
                User.id,
                User.email,
                User.name,
                User.phone_number,
                User.type
            ).where(
                User.email == data["email"],
                User.password == data["password"],
                User.deleted_at == None
            )
        )

        if not users:
            return
        
        token = generate_token({"user_id": users[0]["id"]})
        run_query(
            update(
                User
            ).values({
                "token": token,
            }).where(
                User.id == users[0]['id']
            ), commit=True
        )
        
        users[0]['token'] = token

        return users[0]
