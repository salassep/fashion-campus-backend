from util.db import run_query
from sqlalchemy import insert, select, update, desc
from sqlalchemy.exc import IntegrityError
from model.models import ShippingAddress, ShippingOption

class ShippingService:
    def __init__(self):
        pass

    def get_shipping_address(self, user_id: str) -> dict:
        addresses = run_query(
            select(
                ShippingAddress.id, 
                ShippingAddress.name,
                ShippingAddress.phone_number,
                ShippingAddress.address,
                ShippingAddress.city
            ).where(
                ShippingAddress.user_id == user_id,
                ShippingAddress.deleted_at == None
            ).order_by(
                desc(ShippingAddress.created_at)
            )
        )

        return addresses[0] if addresses else addresses
    
    def get_shipping_address_by_id(self, shipping_address_id:str)-> dict:
        addresses = run_query(
            select(
                ShippingAddress.id, 
                ShippingAddress.name,
                ShippingAddress.phone_number,
                ShippingAddress.address,
                ShippingAddress.city
            ).where(
                ShippingAddress.id == shipping_address_id,
            )
        )

        return addresses[0] if addresses else addresses

    def is_user_address_exist(self, user_id: str) -> bool:
        addresses = run_query(
            select(
                ShippingAddress.id
            ).where(
                ShippingAddress.user_id == user_id,
                ShippingAddress.deleted_at == None
            )
        )

        return True if addresses else False

    def add_shipping_address(self, address_data:dict):
        if self.is_user_address_exist(address_data['user_id']):
            try:
                self.update_shipping_address(address_data)
            except IntegrityError:
                run_query(
                    insert(
                        ShippingAddress
                    ).values(
                        address_data
                    ), commit=True
                )
        else:
            run_query(
                insert(
                    ShippingAddress
                ).values(
                    address_data
                ), commit=True
            )

    def delete_shipping_address(self, shipping_address_id: str):
        run_query(
            update(
                ShippingAddress
            ).values({
                "id": shipping_address_id
            }), commit=True
        )

    def update_shipping_address(self, address_data: dict):
        run_query(
            update(
                ShippingAddress
            ).values(
                address_data
            ).where(
                ShippingAddress.user_id == address_data['user_id'],
                ShippingAddress.deleted_at == None,
            ), commit=True,
        )

    def get_shipping_price(self, total_price: int, method: str = None) -> list:

        shipping_prices = [
            {
                "name": "regular",
                "price": int(total_price * 0.2) if total_price >= 200 else int(total_price * 0.15)
            },
            {
                "name": "next day",
                "price": int(total_price * 0.25) if total_price >= 300 else int(total_price * 0.2)
            }
        ]

        if method:
            return [price['price'] for price in shipping_prices if price['name'] == method][0]

        return shipping_prices

    def get_shipping_option_id(self, method:str) -> str:
        shipping_options = run_query(
            select(
                ShippingOption.id
            ).where(
                ShippingOption.name == method,
                ShippingOption.deleted_at == None,
            )
        )

        return shipping_options[0]['id']

    def get_shipping_option_by_id(self, shipping_option_id:str) -> str:
        shipping_options = run_query(
            select(
                ShippingOption.name
            ).where(
                ShippingOption.id == shipping_option_id,
                ShippingOption.deleted_at == None,
            )
        )

        return shipping_options[0]
