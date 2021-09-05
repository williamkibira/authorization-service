from datetime import datetime, timedelta

import falcon
import simplejson
from jwcrypto import jwk, jwe
from jwcrypto.common import json_encode

from app.core.logging.loggers import LoggerMixin
from app.core.security.password_handler import PasswordHandler
from app.core.storage.storage import FileStorage
from app.domain.authorization.authentication_pb2 import Credentials, Token, UserDetails
from app.domain.authorization.model import User
from app.domain.authorization.repository import AuthorizationRepository
from app.settings import PRIVATE_RSA_KEY


class AuthorizationService(LoggerMixin):
    def __init__(self, file_storage: FileStorage, repository: AuthorizationRepository,
                 password_handler: PasswordHandler,
                 duration: int,
                 base_photo_url: str
                 ):
        self.__base_photo_url = base_photo_url
        self.__duration = duration
        self.__file_storage = file_storage
        self.__repository = repository
        self.__password_handler = password_handler
        self.__key = jwk.JWK()
        with open(PRIVATE_RSA_KEY, "rb") as private_key:
            self.__key.import_from_pem(data=private_key.read())

    def verify_session_request(self, credentials: Credentials) -> Token:
        user = self.__repository.fetch_user_by_email(email=credentials.email)
        if user is not None:
            if not self.__password_handler.verify(input_password=credentials.password, existing_hash=user.password):
                raise falcon.HTTPUnauthorized(title="Your credentials were not a match for an existing user",
                                              description="No matching for {0}".format(credentials.email))
            return self.__create_session(user=user)
        raise falcon.HTTPUnauthorized(title="Your credentials were not a match for an existing user",
                                      description="No matching for {0}".format(credentials.email))

    def fetch_user_details(self, identifier: str) -> UserDetails:
        user = self.__repository.fetch_user_by_identifier(identifier=identifier)
        user_details = UserDetails()
        user_details.identifier = user.identifier
        user_details.first_name = user.first_name
        user_details.last_name = user.last_name
        user_details.email_address = user.email_address
        user_details.photo_url = "{0}/{1}".format(self.__base_photo_url, user.photo_identifier)
        user_details.roles = [role.name for role in user.roles]
        return user_details

    def renew_session(self, identifier: str, device_identifier: str) -> Token:
        user = self.__repository.fetch_user_by_identifier(identifier=identifier)
        current_time = datetime.utcnow()
        expiry_time = current_time + timedelta(days=self.__duration)
        claims = {'sub': identifier,
                  'jti': device_identifier,
                  'exp': expiry_time.timestamp(),
                  'iat': current_time.timestamp(),
                  'roles': [role.name for role in user.roles]}
        protected_header = {
            "alg": "RSA-OAEP-256",
            "enc": "A128CBC-HS256"
        }
        jwe_token = jwe.JWE(simplejson.dumps(claims), json_encode(protected_header))
        jwe_token.add_recipient(key=self.__key)
        content = jwe_token.serialize(compact=True)
        self.__repository.update_session(
            identifier=identifier,
            device_identifier=device_identifier,
            initiated_at=current_time,
            expires_at=expiry_time)
        token = Token()
        token.token = content
        token.expires_in = expiry_time.timestamp() - current_time.timestamp()
        return token

    def end_session(self, identifier: str, device_identifier: str) -> None:
        self.__repository.end_session(identifier=identifier, device_identifier=device_identifier)

    def __create_session(self, user: User, device_identifier: str) -> Token:
        current_time = datetime.utcnow()
        expiry_time = current_time + timedelta(days=self.__duration)
        claims = {'sub': user.identifier,
                  'jti': device_identifier,
                  'exp': expiry_time.timestamp(),
                  'iat': current_time.timestamp(),
                  'roles': [role.name for role in user.roles]}
        protected_header = {
            "alg": "RSA-OAEP-256",
            "enc": "A128CBC-HS256"
        }
        jwe_token = jwe.JWE(simplejson.dumps(claims), json_encode(protected_header))
        jwe_token.add_recipient(key=self.__key)
        content = jwe_token.serialize(compact=True)
        self.__repository.add_session(
            identifier=user.id,
            device_identifier=device_identifier,
            initiated_at=current_time,
            expires_at=expiry_time)
        token = Token()
        token.token = content
        token.expires_in = expiry_time.timestamp() - current_time.timestamp()
        return token

