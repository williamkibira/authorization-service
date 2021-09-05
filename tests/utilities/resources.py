from typing import Dict

import falcon

from app.core.logging.loggers import Logger
from app.core.storage.storage import FileStorage
from app.domain.accounts.emails.client import EmailClient
from app.domain.accounts.emails.orders import AccountDetails, PasswordReset


class FakeFileStorage(FileStorage):
    def __init__(self):
        self.log: Logger = Logger(__file__)
        self.__contents: Dict = {}

    def save(self, identifier: str, content: bytes, content_type: str):
        self.__contents[identifier] = content
        self.log.info("ADDED FOR: {}".format(identifier))

    def fetch(self, response: falcon.Response, identifier: str) -> None:
        response.data = self.__contents[identifier]
        response.content_type = "image/png"
        response.status = falcon.HTTP_OK

    def remove(self, identifier: str):
        del self.__contents[identifier]


class FakeEmailClient(EmailClient):
    def __init__(self, reset_orders: Dict):
        self.__reset_orders = reset_orders

    def send_password_reset(self, order: PasswordReset = None) -> None:
        self._info("EMAIL RESET TO: {} , OTP: {}, REFERENCE: {}".format(order.email, order.otp, order.reference))
        self.__reset_orders[order.reference] = order

    def send_credentials(self, order: AccountDetails = None) -> None:
        self._info("ACCOUNT DETAILS: {} {}".format(order.first_name, order.last_name))
