import datetime
from pydantic import BaseModel, Field


class UserIn(BaseModel):
    name: str = Field(title='Name')
    surname: str = Field(title='Surname')
    email: str = Field(title='Email')
    password: str = Field(title='Password')


class User(UserIn):
    id: int


class ProductIn(BaseModel):
    product_name: str = Field(title='Product_name')
    description: str = Field(title='Description')
    price: float = Field(title='Price')


class Product(ProductIn):
    id: int


class OrderIn(BaseModel):
    user_id: int
    product_id: int
    date: datetime.date
    status: str


class Order(OrderIn):
    id: int
