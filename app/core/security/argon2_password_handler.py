from typing import Dict

from argon2 import PasswordHasher, Type
from argon2.exceptions import VerifyMismatchError

from app.core.security.password_handler import PasswordHandler


class Argon2Configuration(object):
    def __init__(self,
                 memory_cost: int = 102400,
                 salt_length: int = 16,
                 hash_length: int = 16,
                 parallelism: int = 8,
                 time_cost: int = 2,
                 variant: int = 2):
        self.variant: Type = Type(variant)
        self.memory_cost: int = memory_cost
        self.salt_length: int = salt_length
        self.hash_length: int = hash_length
        self.parallelism: int = parallelism
        self.time_cost: int = time_cost

    @staticmethod
    def from_content_map(content_map: Dict):
        return Argon2Configuration(
            memory_cost=int(content_map['argon']['memory-cost']),
            salt_length=int(content_map['argon']['salt-length']),
            hash_length=int(content_map['argon']['hash-length']),
            parallelism=int(content_map['argon']['parallelism']),
            time_cost=int(content_map['argon']['time-cost']),
            variant=int(content_map['argon']['variant'])
        )


class Argon2PasswordHandler(PasswordHandler):

    def __init__(self, configuration: Argon2Configuration) -> None:
        self.__hasher: PasswordHasher = PasswordHasher(
            time_cost=configuration.time_cost,
            parallelism=configuration.parallelism,
            hash_len=configuration.hash_length,
            salt_len=configuration.salt_length,
            memory_cost=configuration.memory_cost,
            type=configuration.variant
        )

    def hash(self, password: str) -> str:
        return self.__hasher.hash(password=password)

    def verify(self, input_password: str, existing_hash: str) -> bool:
        try:
            return self.__hasher.verify(hash=existing_hash, password=input_password)
        except VerifyMismatchError as error:
            print("ERROR: {}".format(error))
            return False
