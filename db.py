from databases import Database
import sqlalchemy
from sqlalchemy.sql.schema import ForeignKey
from settings import settings

db = Database(settings.DATABASE_URL)
mdt = sqlalchemy.MetaData()

users_db = sqlalchemy.Table('users', mdt,
                            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                            sqlalchemy.Column('name', sqlalchemy.String(32)),
                            sqlalchemy.Column('surname', sqlalchemy.String(32)),
                            sqlalchemy.Column('email', sqlalchemy.String(32)),
                            sqlalchemy.Column('password', sqlalchemy.String(100))
                            )

products_db = sqlalchemy.Table('products', mdt,
                               sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                               sqlalchemy.Column('product_name', sqlalchemy.String(64)),
                               sqlalchemy.Column('description', sqlalchemy.String(1000)),
                               sqlalchemy.Column('price', sqlalchemy.Numeric, nullable=False)
                               )

orders_db = sqlalchemy.Table('orders', mdt,
                             sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                             sqlalchemy.Column('user_id', sqlalchemy.ForeignKey('users.id'), nullable=False),
                             sqlalchemy.Column('product_id', sqlalchemy.ForeignKey('products.id'), nullable=False),
                             sqlalchemy.Column('date', sqlalchemy.Date),
                             sqlalchemy.Column('status', sqlalchemy.String(32)),
                             )

engine = sqlalchemy.create_engine(
    settings.DATABASE_URL,
    connect_args={'check_same_thread': False}
)
mdt.create_all(engine)
