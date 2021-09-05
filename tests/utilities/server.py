from typing import Dict

from app.app import ServerApplication
from app.configuration import Configuration
from tests.utilities.resources import FakeFileStorage


class TestServer(ServerApplication):
    def __init__(self, configuration: Configuration, reset_orders: Dict) -> None:
        super(TestServer, self).__init__(configuration=configuration)
        self._reset_orders = reset_orders

    def initialize_resources(self) -> None:
        super(TestServer, self).initialize_resources()
        self._file_storage = FakeFileStorage()
        self._role_repository.save(name="PARTICIPANT")
        self._role_repository.save(name="ADMINISTRATOR")

    def boot_prompt(self):
        build_information = self._configuration.build_information()
        self._info("Starting Test Server {} VER: {}".format(build_information.name(), build_information.version()))
