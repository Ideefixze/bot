from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Numeric, String
from sqlalchemy.orm import sessionmaker, Session

from .Account import BaseAccount

class DatabaseHandler:
    """
        Object responsible for communicating with database for economy cog.
        Can (and should) be made an abstract class and put in other place if we will use
        database connections in other cogs.
    """
    def __init__(self):
        self._engine = create_engine('sqlite:///economy.db', echo=True, future=True)

        BaseAccount.metadata.create_all(self._engine)

        self._session = sessionmaker(bind = self._engine)()

    @property
    def session(self) -> Session:
        return self._session
