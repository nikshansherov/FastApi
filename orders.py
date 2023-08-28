from fastapi import APIRouter, Request
from db import *
from models import *

router = APIRouter()


# Добавление заказа
@router.post('/order/new', response_model=Order)
async def create_order(order: OrderIn):
    query = orders_db.insert().values(
        user_id=order.user_id,
        product_id=order.product_id,
        date=order.date,
        status=order.status
    )
    last_record_id = await db.execute(query)
    return {**order.dict(), 'id': last_record_id}


# Просмотр списка заказов
@router.get('/orders/', response_model=list[Order])
async def read_orders():
    query = orders_db.select()
    return await db.fetch_all(query)


# Просмотр заказа
@router.get('/order/id/{order_id}', response_model=Order)
async def read_orader(order_id: int):
    query = orders_db.select().where(orders_db.c.id == order_id)
    return await db.fetch_one(query)


# Редактирование заказа
@router.put('/order/replace/{order_id}', response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    query = orders_db.update().where(orders_db.c.id == order_id).values(**new_order.dict())
    await db.execute(query)
    return {**new_order.dict(), 'id': order_id}


# Удаление заказа
@router.delete('/order/del/{order_id}')
async def delete_order(order_id: int):
    query = orders_db.delete().where(orders_db.c.id == order_id)
    await db.execute(query)
    return {'message': f'Order {order_id} deleted'}
