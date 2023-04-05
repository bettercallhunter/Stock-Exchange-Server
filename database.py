# import the necessary packages
from sqlalchemy import create_engine, Column, Integer, String, MetaData, ARRAY, Table, JSON
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKeyConstraint, ForeignKey
# create the engine and session
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import desc, PickleType
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
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy_utils import database_exists, create_database

from datetime import datetime
engine = create_engine(
    "postgresql://postgres:0000@localhost:5432/stock?sslmode=disable")
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


class Cancel(Base):
    __tablename__ = 'cancel'
    id = Column(Integer, primary_key=True)
    sym = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    limit = Column(Integer, nullable=False)
    account_id: Mapped[int] = mapped_column(
        ForeignKey("account.id", ondelete='CASCADE'))
    time = Column(DateTime)

    def __repr__(self):
        return f"Order({self.id}, {self.sym}, {self.amount}, {self.limit}, {self.account_id})"


class Executed(Base):
    __tablename__ = 'executed'
    id = Column(Integer, primary_key=True, autoincrement=True)
    transId = Column(Integer, nullable=False)
    sym = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    limit = Column(Integer, nullable=False)
    account_id: Mapped[int] = mapped_column(
        ForeignKey("account.id", ondelete='CASCADE'))
    time = Column(DateTime)

    def __repr__(self):
        return f"Order({self.id}, {self.sym}, {self.amount}, {self.limit}, {self.account_id})"


class Open(Base):
    __tablename__ = 'open'
    id = Column(Integer, primary_key=True)
    sym = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    limit = Column(Integer, nullable=False)
    account_id: Mapped[int] = mapped_column(
        ForeignKey("account.id", ondelete='CASCADE'))
    time = Column(DateTime)

    def __repr__(self):
        return f"Order({self.id}, {self.sym}, {self.amount}, {self.limit}, {self.account_id})"


def init_db():
    Base.metadata.drop_all(engine, checkfirst=True)
    Base.metadata.create_all(engine)


def getMaxId():
    max_cancel_id = session.query(func.max(Cancel.id)).scalar()
    if max_cancel_id is None:
        max_cancel_id = 0
    max_executed_id = session.query(func.max(Executed.id)).scalar()
    if max_executed_id is None:
        max_executed_id = 0
    max_open_id = session.query(func.max(Open.id)).scalar()
    if max_open_id is None:
        max_open_id = 0
    maxId = max(max_cancel_id, max_executed_id, max_open_id)

    return maxId


Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
session = Session()


def closeDb():
    session.close()
    engine.dispose()
