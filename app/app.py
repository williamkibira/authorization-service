import falcon
from decouple import config

from app.configuration import Configuration
from app.core.database.provider import SQLProvider
from app.core.health.health_checks import Readiness, Liveness, Ping
from app.core.security.argon2_password_handler import Argon2PasswordHandler
from app.core.security.password_handler import PasswordHandler
from app.core.server import CoreServerApplication
from app.core.storage.s3_storage import S3FileStorage
from app.core.storage.storage import FileStorage
from app.domain.authorization.repository import AuthorizationRepository
from app.domain.authorization.resource import SessionRequestResource, UserDetailsResource, RenewSession, EndSession
from app.domain.authorization.service import AuthorizationService
from app.domain.authorization.sql_repository import SQLAuthorizationRepository


class ServerApplication(CoreServerApplication):

    def __init__(self, configuration: Configuration):
        self._configuration: Configuration = configuration
        self._repository: AuthorizationRepository = None
        self._password_handler: PasswordHandler = None
        self._authorization_service: AuthorizationService = None

    def initialize_resources(self) -> None:
        database_provider = SQLProvider(
            uri=self._configuration.database_uri(),
            debug=config('DEBUG', default=True, cast=bool))
        database_provider.initialize()
        self._password_handler = Argon2PasswordHandler(
            configuration=self._configuration.argon2_configuration()
        )
        self._repository = SQLAuthorizationRepository(data_source=database_provider.provider())

    def initialize_services(self) -> None:
        self._authorization_service = AuthorizationService(
            base_photo_url=self._configuration.base_photo_url(),
            repository=self._repository,
            password_handler=self._password_handler,
            duration=self._configuration.session_duration()
        )

    def initialize_routes(self, app: falcon.App) -> None:
        app.add_route('/health-check', Readiness())
        app.add_route('/liveness', Liveness())
        app.add_route('/ping', Ping())
        app.add_route('/api/v1/authorization-service/request-session',
                      SessionRequestResource(service=self._authorization_service))
        app.add_route('/api/v1/authorization-service/user-details',
                      UserDetailsResource(service=self._authorization_service))
        app.add_route('/api/v1/authorization-service/renew-session', RenewSession(service=self._authorization_service))
        app.add_route('/api/v1/authorization-service/end-session', EndSession(service=self._authorization_service))

    def boot_prompt(self):
        build_information = self._configuration.build_information()
        self._info("Starting {} VER: {}".format(build_information.name(), build_information.version()))
