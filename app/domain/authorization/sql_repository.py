from datetime import datetime

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

from app.core.database.connection import DataSource
from app.core.logging.loggers import LoggerMixin
from app.domain.authorization.model import User
from app.domain.authorization.repository import AuthorizationRepository


class SQLAuthorizationRepository(AuthorizationRepository, LoggerMixin):
    def __init__(self, data_source: DataSource):
        self.__data_source = data_source

    def add_session(self, identifier: str, device_identifier: str, initiated_at: datetime, expires_at: datetime):
        with self.__data_source.session as session:
            sql: str = "INSERT INTO session_tb(device_identifier, initiated_at, expires_at, user_id) " \
                       "VALUES(:device_identifier, :initiated_at, :expires_at," \
                       "(SELECT id FROM user_tb WHERE identifier=:identifier))"
            session.execute(statement=sql, params={'device_identifier': device_identifier,
                                                   'initiated_at': initiated_at,
                                                   'expires_at': expires_at,
                                                   'identifier': identifier})

    def update_session(self, identifier: str, device_identifier: str, initiated_at: str, expires_at: str):
        with self.__data_source.session as session:
            sql: str = "UPDATE session_tb SET " \
                       "expires_at=:expires_at," \
                       "initiated_at=:initiated_at " \
                       "WHERE device_identifier=:device_identifier " \
                       "AND identifier=:identifier " \
                       "AND status=:status"
            session.execute(statement=sql, params={'device_identifier': device_identifier,
                                                   'initiated_at': initiated_at,
                                                   'expires_at': expires_at,
                                                   'identifier': identifier,
                                                   'status': 'ACTIVE'})

    def end_session(self, identifier: str, device_identifier: str):
        with self.__data_source.session as session:
            sql: str = "UPDATE session_tb SET " \
                       "status=:status " \
                       "WHERE device_identifier=:device_identifier " \
                       "AND identifier=:identifier"
            session.execute(statement=sql, params={'device_identifier': device_identifier,
                                                   'identifier': identifier,
                                                   'status': 'ENDED'})

    def fetch_user_by_identifier(self, identifier: str) -> User:
        try:
            session = self.__data_source.unbound()
            return session.query(User).options(joinedload(User.roles)).filter(User.identifier == identifier).one()
        except NoResultFound as error:
            self._error("ERROR: {}".format(error))
            return None

    def fetch_user_by_email(self, email: str) -> User:
        try:
            session = self.__data_source.unbound()
            return session.query(User).options(joinedload(User.roles)).filter(User.email_address == email).one()
        except NoResultFound as error:
            self._error("ERROR: {}".format(error))
            return None
