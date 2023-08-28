from fastapi import APIRouter, Request
from models import User, UserIn
from db import *

router = APIRouter()


# Наполнение таблицы
@router.get('/fake_users/{count}')
async def create_note(count: int):
    for i in range(1, count + 1):
        query = users_db.insert().values(
            name=f'name_{i}',
            surname=f'surname_{i}',
            email=f'mail_{i}',
            password=f'password_{i}'

        )
        await db.execute(query)
    return {'message': f'{count} fake users create'}


# Добавление пользователя
@router.post('/user/new', response_model=User)
async def create_user(user: UserIn):
    query = users_db.insert().values(
        name=user.name,
        surname=user.surname,
        email=user.email,
        password=user.password,
    )
    last_record_id = await db.execute(query)
    return {**user.dict(), 'id': last_record_id}


# Просмотр списка пользователей
@router.get('/users/', response_model=list[User])
async def read_users():
    query = users_db.select()
    return await db.fetch_all(query)


# Просмотр пользователя
@router.get('/users/id/{user_id}', response_model=User)
async def read_user(user_id: int):
    query = users_db.select().where(users_db.c.id == user_id)
    return await db.fetch_one(query)


# Редактирование пользователя
@router.put('/users/replace/{user_id}', response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users_db.update().where(users_db.c.id == user_id).values(**new_user.dict())
    await db.execute(query)
    return {**new_user.dict(), 'id': user_id}


# Удаление пользователя
@router.delete('/users/del/{user_id}')
async def delete_user(user_id: int):
    query = users_db.delete().where(users_db.c.id == user_id)
    await db.execute(query)
    return {'message': f'User {user_id} deleted'}
