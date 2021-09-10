import falcon

from app.app import ServerApplication
from app.configuration import Configuration


def run() -> falcon.App:
    application = ServerApplication(configuration=Configuration.get_instance())
    return application.run()


win_app = run()
