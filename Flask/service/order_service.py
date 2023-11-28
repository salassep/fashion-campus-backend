import uuid

from util.db import run_query
from sqlalchemy import insert, select, update, desc
from model.models import Order, Cart, CartOrder, Product, User

class OrderService:
    def __init__(self):
        pass

    def create_order(self, order_data: dict):
        run_query(
            insert(
                Order
            ).values(
                order_data
            ), commit=True
        )

        ordered_carts = run_query(
            select(
                Cart.id.label('cart_id')
            ).where(
                Cart.user_id == order_data['user_id'],
                Cart.ordered_at == None,
                Cart.deleted_at == None
            )
        )

        for index, cart in enumerate(ordered_carts):
            ordered_carts[index]['id'] = uuid.uuid4()
            ordered_carts[index]['order_id'] = order_data['id']

        run_query(
            insert(
                CartOrder
            ).values(
                ordered_carts
            ), commit=True
        )
    
    def get_orders(self, user_id: str) -> list :
        orders = run_query(
            select(
                Order.id,
                Order.shipping_option_id,
                Order.shipping_address_id,
                Order.status,
                Order.created_at,
            ).where(
                Order.user_id == user_id,
                Order.deleted_at == None,
            )
        )

        for index,order in enumerate(orders) :
            cart_order = self.get_cart_orders(order['id'])
            orders[index]['products'] = cart_order

        return orders
    
    def get_admin_orders(self, filter_order_data: dict):
        # SELECT cart_orders.id, orders.created_at, products.product_name AS title, carts.size, products.description, users.email, users.id AS user_id, products.price, carts.quantity, orders.shipping_option_id
        # FROM cart_orders 
        # JOIN carts ON cart_orders.cart_id = carts.id
        # JOIN orders ON cart_orders.order_id = orders.id
        # JOIN products ON carts.product_id = products.id
        # JOIN users ON carts.user_id = users.id
        sort_by = filter_order_data["sort_by"]
        page = filter_order_data['page']
        page_size = filter_order_data['page_size']

        query = select(
            [Order.id,
            Order.created_at,
            User.email,
            User.name,
            User.id.label('user_id'),
            Order.total_order,
            Order.status]
        ).join(
            User, User.id == Order.user_id
        ).where(
            Order.deleted_at == None
        )
        
        if sort_by: 
            sort = sort_by.lower()
            if sort == "price a_z":
                query = query.order_by(Order.total_order)
            elif sort == "price z_a":
                query = query.order_by(desc(Order.total_order))
                
        try:
            page = int(page)
            page_size = int(page_size)
        except:
            page = 1
            page_size = 10

        data = run_query(query)

        try:
            data_send = [data[i:i+page_size] for i in range(0, len(data), page_size)][page-1]
        except IndexError:
            data_send = []

        return data_send

    def get_cart_orders(self, order_id:str) -> dict :
        cart_orders = run_query(
            select(
                Cart.id,
                Cart.quantity,
                Cart.size,
                Cart.product_id,
                Product.product_name,
                Product.price,
            ).join(
                CartOrder, CartOrder.cart_id == Cart.id
            ).join(
                Product, Product.id == Cart.product_id
            ).where(
                CartOrder.order_id == order_id,
                Cart.deleted_at == None,
            )
        )

        return cart_orders
    
    def update_status_order(self, order_data: dict):
        run_query(
            update(
                Order
            ).values(
                order_data
            ).where(
                Order.id == order_data['id'],
                Order.deleted_at == None,
            ), commit=True,
        )