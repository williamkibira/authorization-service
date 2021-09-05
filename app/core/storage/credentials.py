from typing import Dict


class S3Credentials(object):
    def __init__(self, content_map: Dict):
        self.__key: str = content_map['aws']['access-key']
        self.__secret: str = content_map['aws']['secret-key']
        self.__bucket: str = content_map['aws']['bucket']
        self.__region: str = content_map['aws']['region']
        self.__url: str = content_map['aws']['url']

    def key(self):
        return self.__key

    def secret(self):
        return self.__secret

    def bucket(self):
        return self.__bucket

    def region(self):
        return self.__region

    def url(self):
        return self.__url
