from app.core.logging.loggers import LoggerMixin
from app.core.storage.storage import FileStorage
from app.domain.authorization.authentication_pb2 import Credentials, Token, UserDetails
from app.domain.authorization.repository import AuthorizationRepository


class AuthorizationService(LoggerMixin):
    def __init__(self, file_storage: FileStorage, repository: AuthorizationRepository):
        self.__file_storage = file_storage
        self.__repository = repository

    def verify_session_request(self, credentials: Credentials) -> Token:
        pass

    def fetch_user_details(self, identifier: str) -> UserDetails:
        pass

    def renew_session(self, previous_token: str) -> Token:
        pass

    def end_session(self, access_token: str) -> None:
        pass



