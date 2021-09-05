import abc
from datetime import datetime

from app.domain.authorization.model import User


class AuthorizationRepository(abc.ABC):
    @abc.abstractmethod
    def add_session(self, identifier: str, device_identifier: str, initiated_at: datetime, expires_at: datetime):
        pass

    @abc.abstractmethod
    def update_session(self, identifier: str, device_identifier: str, initiated_at: str, expires_at: str):
        pass

    @abc.abstractmethod
    def end_session(self, identifier: str, device_identifier: str):
        pass

    @abc.abstractmethod
    def fetch_user_by_identifier(self, identifier: str) -> User:
        pass

    @abc.abstractmethod
    def fetch_user_by_email(self, email: str) -> User:
        pass
