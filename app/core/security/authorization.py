from datetime import datetime
from typing import List

import falcon
import simplejson as json
from jwcrypto import jwk, jwe

from app.core.security.claims import Claims
from app.settings import PRIVATE_RSA_KEY


class Restrict(object):
    def __init__(self, roles: List[str]):
        self.__roles = roles

    def __call__(self, req: falcon.Request, resp: falcon.Response, resource, params):
        token = self.__strip_out_authorization_token(req=req)
        claims_payload = self.__extract_token_claims(encrypted_token=token)
        claims = Claims.parse(claims_payload)
        if self.__is_authorized(claims=claims):
            req.context["principals"] = claims
            req.context["access_token"] = token
        else:
            raise falcon.HTTPForbidden(title="No Authorization for this request",
                                       description="You do not have the required permissions to access this resource")

    def __is_authorized(self, claims: Claims) -> bool:
        if self.__roles is []:
            return True
        return claims.has_roles(roles=self.__roles)

    def __extract_token_claims(self, encrypted_token: str) -> str:
        jwe_token = jwe.JWE()
        private_key = self.__read_private_key(path=PRIVATE_RSA_KEY)
        jwe_token.deserialize(encrypted_token, key=private_key)
        return jwe_token.payload

    @staticmethod
    def __strip_out_authorization_token(req: falcon.Request) -> str:
        if req.get_header('Authorization') is None:
            raise falcon.HTTPUnauthorized(title="No Authorization for this request",
                                          description="You haven't added `Authorization` to this request")
        return req.get_header('Authorization').split(" ")[1]

    @staticmethod
    def __read_private_key(path: str) -> jwk.JWK:
        with open(path, "rb") as private_key_file:
            key = jwk.JWK()
            key.import_from_pem(data=private_key_file.read())
            return key

    @staticmethod
    def __verify_claim(claim: Claims) -> None:
        # if ACCEPTED_AUDIENCE.trim() in claim['aud']:
        #     raise falcon.HTTPForbidden(title="This user is not permitted to access this service",
        #                                description="You are not the intended audience for this service")
        if claim.expiry() < datetime.datetime.now():
            raise falcon.HTTPUnauthorized(title="Your session has expired",
                                          description="Your current session is past its duration. \n"
                                                      "Please login again to continue")
