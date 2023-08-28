import uvicorn
from fastapi import FastAPI
import users, products, orders
from db import db

app = FastAPI()


@app.on_event('startup')
async def startup():
    await db.connect()


@app.on_event('shutdown')
async def shutdown():
    await db.disconnect()


app.include_router(users.router, tags=['Users'])
app.include_router(products.router, tags=['Products'])
app.include_router(orders.router, tags=['Orders'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='127.0.0.1',
        port=8000,
        reload=True
    )
