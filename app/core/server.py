import abc

import falcon
from prometheus_client import CollectorRegistry
from app.core.logging.loggers import LoggerMixin
from app.core.middleware.prometheus import PrometheusMiddleware


class CoreServerApplication(abc.ABC, LoggerMixin):

    @abc.abstractmethod
    def initialize_resources(self) -> None:
        pass

    @abc.abstractmethod
    def initialize_routes(self, app: falcon.App) -> None:
        pass

    @abc.abstractmethod
    def initialize_services(self) -> None:
        pass

    @abc.abstractmethod
    def boot_prompt(self):
        pass

    def run(self) -> falcon.App:
        app: falcon.App = falcon.App(
            cors_enable=True,
            middleware=[
                PrometheusMiddleware(register=CollectorRegistry()),
            ])
        self.initialize_resources()
        self.initialize_services()
        self.initialize_routes(app)
        self.boot_prompt()
        return app
