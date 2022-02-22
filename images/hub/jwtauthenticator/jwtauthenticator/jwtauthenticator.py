from typing import Union, Any

from firstuseauthenticator import FirstUseAuthenticator
from firstuseauthenticator.firstuseauthenticator import CustomLoginHandler, ResetPasswordHandler
from jose import jwt
from jupyterhub.auth import LocalAuthenticator, DummyAuthenticator, Authenticator
from jupyterhub.handlers import BaseHandler, LoginHandler
from jupyterhub.utils import url_path_join
from tornado import gen, web
from tornado.web import MissingArgumentError
from traitlets import Unicode, Bool

import time


class JSONWebTokenLoginHandler(BaseHandler):

    def get(self):
        header_name = self.authenticator.header_name
        param_name = self.authenticator.param_name
        header_is_authorization = self.authenticator.header_is_authorization

        auth_header_content = self.request.headers.get(header_name, "")
        auth_cookie_content = self.get_cookie("XSRF-TOKEN", "")
        signing_certificate = self.authenticator.signing_certificate
        secret = self.authenticator.secret
        username_claim_field = self.authenticator.username_claim_field
        timestamp_claim_field = self.authenticator.timestamp_claim_field
        timeout = self.authenticator.param_timeout
        audience = self.authenticator.expected_audience
        tokenParam = self.get_argument(param_name, default=False)

        if auth_header_content and tokenParam:
            raise web.HTTPError(400)
        elif auth_header_content:
            if header_is_authorization:
                # we should not see "token" as first word in the AUTHORIZATION header, if we do it could mean someone coming in with a stale API token
                if auth_header_content.split()[0] != "bearer":
                    raise web.HTTPError(403)
                token = auth_header_content.split()[1]
            else:
                token = auth_header_content
        elif auth_cookie_content:
            token = auth_cookie_content
        elif tokenParam:
            token = tokenParam
        else:
            raise web.HTTPError(401)

        claims = "";
        if secret:
            claims = self.verify_jwt_using_secret(token, secret, audience)
        elif signing_certificate:
            claims = self.verify_jwt_with_claims(token, signing_certificate, audience)
        else:
            raise web.HTTPError(401)

        timestamp = self.retrieve_timestamp(claims, timestamp_claim_field)
        timenow = int(time.time())
        if timenow - int(timestamp) > int(timeout):
            raise web.HTTPError(401)

        username = self.retrieve_username(claims, username_claim_field)
        user = self.user_from_username(username)
        self.set_login_cookie(user)

        _url = url_path_join(self.hub.server.base_url, 'spawn/'+ username)
        next_url = self.get_argument('next', default=False)
        if next_url:
            _url = next_url

        self.redirect(_url)

    def set_login_cookie(self, user):
        """
        重写set_login_cookie用于不用用户登录
        """
        """Set login cookies for the Hub and single-user server."""
        if self.subdomain_host and not self.request.host.startswith(self.domain):
            self.log.warning(
                "Possibly setting cookie on wrong domain: %s != %s",
                self.request.host,
                self.domain,
            )

        # set single cookie for services
        self.set_service_cookie(user)
        self.set_session_cookie()
        # create and set a new cookie token for the hub
        self.set_hub_cookie(user)

    def set_secure_cookie(self, name: str, value: Union[str, bytes], expires_days: int = 30, version: int = None,
                          **kwargs: Any) -> None:
        expires_days = None
        super().set_secure_cookie(name, value, expires_days, version, **kwargs)

    @staticmethod
    def verify_jwt_with_claims(token, signing_certificate, audience):
        # If no audience is supplied then assume we're not verifying the audience field.
        if audience == "":
            opts = {"verify_aud": False}
        else:
            opts = {}
        with open(signing_certificate, 'r') as rsa_public_key_file:
            return jwt.decode(token, rsa_public_key_file.read(), audience=audience, options=opts)

    @staticmethod
    def verify_jwt_using_secret(json_web_token, secret, audience):
        # If no audience is supplied then assume we're not verifying the audience field.
        if audience == "":
            opts = {"verify_aud": False}
        else:
            opts = {}

        return jwt.decode(json_web_token, secret, algorithms=list(jwt.ALGORITHMS.SUPPORTED), audience=audience,
                          options=opts)

    @staticmethod
    def retrieve_username(claims, username_claim_field):
        # retrieve the username from the claims
        username = claims[username_claim_field]
        if "@" in username:
            # process username as if email, pull out string before '@' symbol
            return username.split("@")[0]

        else:
            # assume not username and return the user
            return username

    @staticmethod
    def retrieve_timestamp(claims, timestamp_claim_field):
        # retrieve the username from the claims
        timestamp = claims[timestamp_claim_field]

        return timestamp

class JSONWebTokenAuthenticator(Authenticator):
    """
    Accept the authenticated JSON Web Token from header.
    """
    signing_certificate = Unicode(
        config=True,
        help="""
        The public certificate of the private key used to sign the incoming JSON Web Tokens.

        Should be a path to an X509 PEM format certificate filesystem.
        """
    )

    username_claim_field = Unicode(
        default_value='upn',
        config=True,
        help="""
        The field in the claims that contains the user name. It can be either a straight username,
        of an email/userPrincipalName.
        """
    )

    timestamp_claim_field = Unicode(
        default_value='3600',
        config=True,
        help="""The field in the claims that contains timestamp.""")
    
    expected_audience = Unicode(
        default_value='',
        config=True,
        help="""HTTP header to inspect for the authenticated JSON Web Token."""
    )

    header_name = Unicode(
        default_value='Authorization',
        config=True,
        help="""HTTP header to inspect for the authenticated JSON Web Token.""")

    header_is_authorization = Bool(
        default_value=True,
        config=True,
        help="""Treat the inspected header as an Authorization header.""")

    param_name = Unicode(
        config=True,
        default_value='access_token',
        help="""The name of the query parameter used to specify the JWT token""")

    param_timeout = Unicode(
        config=True,
        default_value='60',
        help="""The name of the query parameter used to specify the JWT token timeout time""")

    secret = Unicode(
        config=True,
        help="""Shared secret key for siging JWT token.  If defined, it overrides any setting for signing_certificate""")

    def get_handlers(self, app):
        return [
            (r'/login', JSONWebTokenLoginHandler),
        ]

    @gen.coroutine
    def authenticate(self, *args):
        raise NotImplementedError()


class JSONWebTokenLocalAuthenticator(JSONWebTokenAuthenticator, LocalAuthenticator):
    """
    A version of JSONWebTokenAuthenticator that mixes in local system user creation
    """
    pass


class MyDummyAuthenticator(DummyAuthenticator):
    def get_handlers(self, app):
        return [('/login2', LoginHandler)]



class MyFirstuseauthenticator(FirstUseAuthenticator):
    def get_handlers(self, app):
        return [
            (r"/login2", CustomLoginHandler),
            (r"/auth/change-password", ResetPasswordHandler),
        ]

class BlendAuthenticator(JSONWebTokenAuthenticator, MyFirstuseauthenticator):
    def get_handlers(self, app):
        handlers = JSONWebTokenAuthenticator.get_handlers(self, app) + MyFirstuseauthenticator.get_handlers(self, app)
        self.log.info(handlers)
        return handlers

    # @gen.coroutine
    def authenticate(self, handler, data=None):
        authenticator = None
        self.log.info(type(handler))
        try:
            handler.get_argument("auth_token")
            authenticator = JSONWebTokenAuthenticator.authenticate(self, handler, data)
        except MissingArgumentError:
            authenticator = MyFirstuseauthenticator.authenticate(self, handler, data)
        return authenticator
