from fastapi import APIRouter, Request
from models import Product, ProductIn
from db import *

router = APIRouter()


# Наполнение таблицы
@router.get('/fake_products/{count}')
async def create_products(count: int):
    for i in range(1, count + 1):
        query = products_db.insert().values(
            product_name=f'product_{i}',
            description=f'description_{i}',
            price=i * 100
        )
        await db.execute(query)
    return {'message': f'{count} fake products create'}


# Добавление продукта
@router.post('/product/new', response_model=Product)
async def create_product(product: ProductIn):
    query = products_db.insert().values(
        product_name=product.product_name,
        description=product.description,
        price=product.price
    )
    last_record_id = await db.execute(query)
    return {**product.dict(), 'id': last_record_id}


# Просмотр списка продуктов
@router.get('/products/', response_model=list[Product])
async def read_products():
    query = products_db.select()
    return await db.fetch_all(query)


# просмотр одного продукта
@router.get('/product/id/{product_id}', response_model=Product)
async def read_product(product_id: int):
    query = products_db.select().where(products_db.c.id == product_id)
    return await db.fetch_one(query)


# Редактирование продукта
@router.put('/product/replace/{product_id}', response_model=Product)
async def update_product(product_id: int, new_product: ProductIn):
    query = products_db.update().where(products_db.c.id == product_id).values(**new_product.dict())
    await db.execute(query)
    return {**new_product.dict(), 'id': product_id}


# Удаление продукта
@router.delete('/product/del/{product_id}')
async def delete_product(product_id: int):
    query = products_db.delete().where(products_db.c.id == product_id)
    await db.execute(query)
    return {'message': f'Poduct {product_id} deleted'}
