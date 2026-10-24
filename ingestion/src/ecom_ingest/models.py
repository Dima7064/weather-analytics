from datetime import date, datetime

from pydantic import BaseModel


class Customer(BaseModel):
    customer_id: int
    name: str
    country: str
    signup_date: date


class Product(BaseModel):
    product_id: int
    name: str
    category: str
    price: float


class Order(BaseModel):
    order_id: int
    customer_id: int
    product_id: int
    quantity: int
    status: str
    order_date: datetime
