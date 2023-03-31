# import the necessary packages
from sqlalchemy import create_engine, Column, Integer, String, MetaData, ARRAY, Table, JSON
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKeyConstraint, ForeignKey
# create the engine and session
from sqlalchemy import desc
from sqlalchemy import create_engine
from sqlalchemy import select
from typing import List
from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
# set up the connection parameters
from sqlalchemy import create_engine

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

engine = create_engine("postgresql://postgres:0000@localhost:5432/stock")
if not database_exists(engine.url):
    create_database(engine.url)


# meta = MetaData()
# account = Table(
#     'account', meta,
#     Column('id', Integer, primary_key=True),
#     Column('balance', Integer, nullable=False),
#     Column('position', ARRAY(String)),
# )
# symbol = Table(
#     'symbol', meta,
#     Column('id', Integer, primary_key=True),
#     Column('sym', String, nullable=False),
#     Column('number', Integer, nullable=False),
#     Column('account', Integer, nullable=False),
#     # add foreign key constraint
#     ForeignKeyConstraint(['account'], ['account.id']),

# )
# meta.drop_all(engine, checkfirst=True)
# meta.create_all(engine)


# create models
class Base(DeclarativeBase):
    pass


class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    balance = Column(Integer, nullable=False)
    position = Column(JSON)


class Symbol(Base):
    __tablename__ = 'symbol'
    id = Column(Integer, primary_key=True)
    sym = Column(String, nullable=False)
    number = Column(Integer, nullable=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))


Base.metadata.drop_all(engine, checkfirst=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
