from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session

from app.core.database.base import BaseModel
from app.core.database.connection import DataSource


class SQLProvider(object):
    def __init__(self, uri: str, debug: bool = False) -> None:
        self.__uri = uri
        self.__engine: Engine
        self.__debug = debug
        self.__session: Session = None

    def initialize(self):
        self.__engine = create_engine(
            self.__uri,
            echo=self.__debug
        )
        session_factory = sessionmaker(bind=self.__engine)
        self.__session = scoped_session(session_factory=session_factory)
        BaseModel.set_session(session=self.__session)
        BaseModel.prepare(self.__engine, reflect=True)

    def provider(self) -> DataSource:
        return DataSource(session=self.__session)
