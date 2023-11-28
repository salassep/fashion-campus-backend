from datetime import datetime
from util.db import run_query
from sqlalchemy import select, insert, update, desc
from sqlalchemy.exc import IntegrityError
from model.models import Cart, Product

class CartService:
    def __init__(self):
        pass

    def add_to_cart(self, data: dict):
        cart = self.check_product_in_cart(data["user_id"], data['product_id'], data['size'])
        if not cart:
            try:
                run_query(
                    insert(
                        Cart
                    ).values(
                        data
                    ), commit=True
                )
            except IntegrityError as e:
                raise Exception("Product not found")
        else:
            self.add_product_quantity(cart['id'], data['quantity'])


    def is_cart_exists_by_user_or_cart_id(self, id: str) -> bool:
        carts = run_query(
            select(
                Cart.id
            ).where(
                (Cart.user_id == id) | (Cart.id == id),
                Cart.ordered_at == None,
                Cart.deleted_at == None
            )
        )

        return True if carts else False

    def add_product_quantity(self, cart_id: str, quantity: int):
        current_quantity = run_query(
            select(
                Cart.quantity
            ).where(
                Cart.id == cart_id
            )
        )[0]['quantity']
        
        run_query(
            update(
                Cart
            ).values({
                'quantity': current_quantity + quantity 
            }).where(
                Cart.id == cart_id
            ), commit=True
        )

    def check_product_in_cart(self, user_id: str, product_id: str, size: str):
        carts = run_query(
            select(Cart.id)
            .where(
                Cart.user_id == user_id,
                Cart.product_id == product_id,
                Cart.size == size,
                Cart.deleted_at == None,
                Cart.ordered_at == None
            )
        )

        return carts[0] if carts else None

    def get_cart_by_id(self, cart_id:str)-> list:
        carts = run_query(
            select(
                Cart.id,
                Cart.quantity,
                Cart.size,
                Cart.product_id,
                Product.price,
                Product.product_name
            ).join(
                Product, Product.id == Cart.product_id
            ).where(
                Cart.id == cart_id,
            )
        )

        return carts

    def get_user_carts(self, user_id: str):
        carts = run_query(
            select(
                Cart.id,
                Cart.quantity,
                Cart.size,
                Cart.product_id,
                Product.price,
                Product.product_name
            ).join(
                Product, Product.id == Cart.product_id
            ).where(
                Cart.user_id == user_id,
                Cart.ordered_at == None,
                Cart.deleted_at == None,
            ).order_by(
                desc(Cart.created_at)
            )
        )
        
        return carts

    def get_cart_total_price(self, user_id: str) -> int:
        cart_prices = run_query(
            select(
                Cart.quantity,
                Product.price,
            ).join(
                Product, Product.id == Cart.product_id
            ).where (
                Cart.user_id == user_id,
                Cart.ordered_at == None,
                Cart.deleted_at == None, 
                Product.deleted_at == None
            )
        )

        if not cart_prices:
            return

        total_price = sum(
            [cart_price['price']*cart_price['quantity'] for cart_price in cart_prices]
        )

        return total_price

    def checkout_cart(self, user_id: str):
        time_now = datetime.now()
        run_query(
            update(
                Cart
            ).values({
                "updated_at": time_now,
                "ordered_at": time_now
            }).where(
                Cart.user_id == user_id,
                Cart.ordered_at == None,
                Cart.deleted_at == None
            ), commit=True
        )

    def delete_cart(self, cart_id: str):
        time_now = datetime.now()
        run_query(
            update(
                Cart
            ).values({
                "deleted_at": time_now
            }).where(
                Cart.id == cart_id,
            ), commit=True
        )
