import uuid
import datetime
from sqlalchemy import (
    Column,
    ForeignKey,
    DateTime,
    Integer,
    String,
    Text,
    text
)
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class TimeStamp:
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

class User(Base, TimeStamp):
    __tablename__ = 'users'

    id = Column(String, nullable=False, primary_key=True, default=uuid.uuid4())
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    image = Column(String, unique=True)
    phone_number = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    token = Column(String, nullable=True, unique=True)
    type = Column(String, server_default=text("'buyer'"))
    balance = Column(Integer, server_default=text("0"))

class Category(Base, TimeStamp):
    __tablename__ = 'categories'

    id = Column(String, nullable=False, primary_key=True, default=uuid.uuid4())
    category_name = Column(String, nullable=False, unique=True)
    image = Column(String, nullable=True)

class Product(Base, TimeStamp):
    __tablename__ = 'products'

    id = Column(String, nullable=False, primary_key=True, default=uuid.uuid4())
    category_id = Column(String, ForeignKey("categories.id"))
    product_name =  Column(String, nullable=False)
    description = Column(Text)
    condition = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    view = Column(Integer, server_default=text("0"))

class ProductImage(Base, TimeStamp):
    __tablename__ = 'product_images'

    id = Column(String, nullable=False, primary_key=True, default=uuid.uuid4())
    product_id = Column(String, ForeignKey("products.id"))
    image =  Column(String, nullable=True)

class Cart(Base, TimeStamp):
    __tablename__ = 'carts'

    id = Column(String, nullable=False, primary_key=True, default=uuid.uuid4())
    user_id = Column(String, ForeignKey("users.id"))
    product_id = Column(String, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    size = Column(String, nullable=False)
    ordered_at = Column(DateTime, nullable=True)

class Banner(Base, TimeStamp):
    __tablename__ = 'banners'

    id = Column(String, nullable=False, primary_key=True, default=uuid.uuid4())
    image = Column(String, nullable=True)
    title = Column(String, nullable=True)

class ShippingAddress(Base, TimeStamp):
    __tablename__ = 'shipping_addresses'

    id = Column(String, nullable=False, primary_key=True, default=uuid.uuid4())
    user_id = Column("user_id", String, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String)

class ShippingOption(Base, TimeStamp):
    __tablename__ = 'shipping_options'

    id = Column(String, nullable=False, primary_key=True, default=uuid.uuid4())
    name = Column(String, nullable=False, unique=True)

class Order(Base, TimeStamp):
    __tablename__ = 'orders'
    
    id = Column(String, nullable=False, primary_key=True, default=uuid.uuid4())
    user_id = Column(String, ForeignKey("users.id"))
    shipping_address_id =  Column(String, ForeignKey("shipping_addresses.id"))
    shipping_option_id = Column(String, ForeignKey("shipping_options.id"))
    status = Column(String, nullable=False)
    total_order = Column(Integer, nullable=False)

class CartOrder(Base):
    __tablename__ = 'cart_orders'

    id = Column(String, nullable=False, primary_key=True, default=uuid.uuid4())
    cart_id = Column(String, ForeignKey("carts.id"))
    order_id = Column(String, ForeignKey("orders.id"))

class Wishlist(Base):
    __tablename__ = 'wishlist'
    
    id = Column(String, nullable=False, primary_key=True, default=uuid.uuid4())
    user_id = Column(String, ForeignKey("users.id"))
    product_id = Column(String, ForeignKey("products.id"))