import abc


class PasswordHandler(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'hash') and
                callable(subclass.hash) and
                hasattr(subclass, 'verify') and
                callable(subclass.verify) or
                NotImplemented)

    @abc.abstractmethod
    def hash(self, password: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def verify(self, input_password: str, existing_hash: str) -> bool:
        raise NotImplementedError
