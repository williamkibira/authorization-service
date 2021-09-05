import abc

import falcon


class FileStorage(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'save') and
                callable(subclass.save) and
                hasattr(subclass, 'fetch') and
                callable(subclass.fetch) and
                hasattr(subclass, 'remove') and
                callable(subclass.remove) or
                NotImplemented)

    @abc.abstractmethod
    def save(self, identifier: str, content: bytes, content_type: str):
        raise NotImplementedError

    @abc.abstractmethod
    def fetch(self, response: falcon.Response, identifier: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, identifier: str):
        raise NotImplementedError
