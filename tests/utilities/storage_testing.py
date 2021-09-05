import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.configuration import Configuration
from app.core.database.base import BaseModel
from app.core.database.migrations import SQLMigrationHandler
from app.settings import MIGRATIONS_FOLDER


class DatabaseResourceTests(unittest.TestCase):

    def setUp(self) -> None:
        configuration: Configuration = Configuration.get_instance(testing=True)
        self.migration_handler = SQLMigrationHandler(
            database_url=configuration.database_uri(),
            migration_folder=MIGRATIONS_FOLDER
        )
        self.migration_handler.migrate()
        self.__debug = True
        engine = create_engine(
            configuration.database_uri(),
            echo=self.__debug
        )
        session_factory = sessionmaker(bind=engine)
        self.session = scoped_session(session_factory)
        BaseModel.set_session(session=self.session)
        BaseModel.prepare(engine, reflect=True)

    def tearDown(self) -> None:
        self.migration_handler.rollback()
