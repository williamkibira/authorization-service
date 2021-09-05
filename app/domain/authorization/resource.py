import falcon

from app.core.security.authorization import Restrict
from app.domain.authorization.authentication_pb2 import Credentials
from app.domain.authorization.service import AuthorizationService


class SessionRequestResource(object):
    def __init__(self, service: AuthorizationService):
        self.__service = service

    def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        credentials = Credentials()
        credentials.ParseFromString(req.bounded_stream.read())
        token = self.__service.verify_session_request(credentials=credentials)
        resp.body = token.SerializeToString()
        resp.content_type = "application/x-protobuf"
        resp.status = falcon.HTTP_OK


@falcon.before(Restrict(roles=['PARTICIPANT']))
class UserDetailsResource(object):
    def __init__(self, service: AuthorizationService):
        self.__service = service

    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        principals = req.context["principals"]
        user_details = self.__service.fetch_user_details(identifier=principals.subject())
        resp.body = user_details.SerializeToString()
        resp.content_type = "application/x-protobuf"
        resp.status = falcon.HTTP_OK


@falcon.before(Restrict(roles=['PARTICIPANT']))
class RenewSession(object):
    def __init__(self, service: AuthorizationService):
        self.__service = service

    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        token = self.__service.renew_session(previous_token=req.context["access_token"])
        resp.body = token.SerializeToString()
        resp.content_type = "application/x-protobuf"
        resp.status = falcon.HTTP_OK


@falcon.before(Restrict(roles=['PARTICIPANT']))
class EndSession(object):
    def __init__(self, service: AuthorizationService):
        self.__service = service

    def on_put(self, req: falcon.Request, resp: falcon.Response) -> None:
        self.__service.end_session(access_token=req.context["access_token"])
        resp.status = falcon.HTTP_NO_CONTENT
