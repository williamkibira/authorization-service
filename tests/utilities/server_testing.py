import unittest
from datetime import datetime, timedelta
from typing import List, Dict

import simplejson
from falcon.testing import TestClient
from jwcrypto import jwk, jwe
from jwcrypto.common import json_encode

from app.configuration import Configuration
from app.core.database.migrations import SQLMigrationHandler
from app.settings import MIGRATIONS_FOLDER, PRIVATE_RSA_KEY
from tests.utilities.server import TestServer


class ServerTestCase(unittest.TestCase, TestClient):
    _reset_orders: Dict

    def setUp(self) -> None:
        super(ServerTestCase, self).setUp()
        self._reset_orders = {}
        self.application = TestServer(configuration=self.configuration(), reset_orders=self._reset_orders)
        self.migration_handler = SQLMigrationHandler(
            database_url=self.configuration().database_uri(),
            migration_folder=MIGRATIONS_FOLDER
        )
        self.migration_handler.migrate()
        TestClient.__init__(self, self.application.run())

    def tearDown(self) -> None:
        self.migration_handler.rollback()

    @staticmethod
    def configuration():
        return Configuration.get_instance(testing=True)

    @staticmethod
    def read_public_key() -> jwk.JWK:
        with open(PRIVATE_RSA_KEY, "rb") as public_key_file:
            key = jwk.JWK()
            key.import_from_pem(data=public_key_file.read(), password=None)
            return key

    def authorization_for(self, identifier: str, roles: List[str]) -> str:
        current_time = datetime.utcnow()
        expiry_time = current_time + timedelta(hours=10)
        claims = {
            'aud': 'localhost',
            'sub': identifier,
            'jti': identifier,
            'roles': roles,
            'exp': expiry_time.timestamp(),
            'iat': current_time.timestamp()
        }
        key = self.read_public_key()
        protected_header = {
            "alg": "RSA-OAEP-256",
            "enc": "A128CBC-HS256"
        }
        token = jwe.JWE(simplejson.dumps(claims), json_encode(protected_header))
        token.add_recipient(key=key)
        return "Bearer {0}".format(token.serialize(compact=True))
