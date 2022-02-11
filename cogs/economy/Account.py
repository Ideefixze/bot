from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Numeric
BaseAccount = declarative_base()


class Account(BaseAccount):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    money = Column(Numeric(10,2))