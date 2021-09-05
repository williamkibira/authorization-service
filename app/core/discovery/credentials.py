from decouple import config


class Credentials(object):
    def __init__(self):
        self.__host: str = config('CONSUL_HOST', default='localhost')
        self.__port: int = config('CONSUL_PORT', default=8500, cast=int)
        self.__datacenter: str = config('CONSUL_DATACENTER', default='dc1')
        self.__token: str = config('CONSUL_TOKEN', default='')

    def host(self) -> str:
        return self.__host

    def port(self) -> int:
        return self.__port

    def datacenter(self) -> str:
        return self.__datacenter

    def token(self):
        return self.__token