from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Numeric, String
from sqlalchemy.orm import sessionmaker, DeclarativeMeta


class DatabaseHandler:
    """
        Object responsible for communicating with database cogs.
    """
    def __init__(self,address='sqlite:///database.db', bases:list[DeclarativeMeta]=[]):
        self._engine = create_engine(address, echo=True, future=True)

        for base in bases:
            base.metadata.create_all(self._engine)

        self._sessionmaker = sessionmaker(bind = self._engine)

    @property
    def session(self) -> sessionmaker:
        return self._sessionmaker

