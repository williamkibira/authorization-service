import falcon
from falcon import Request, Response
import simplejson as json
from datetime import datetime

from app.configuration import BuildInformation


class Readiness(object):
    def on_get(self, req: Request, resp: Response) -> None:
        start = datetime.now()
        self.session.commit()
        duration = int((datetime.now() - start).total_seconds() * 1000000)
        resp.body = json.dumps({
            'id': 0,
            'sql': 'ok',
            'sql_duration': duration
        })
        resp.status = falcon.HTTP_OK


class Liveness(object):
    def on_get(self, req: Request, resp: Response) -> None:
        start = datetime.now()
        self.session.commit()
        duration = int((datetime.now() - start).total_seconds() * 1000000)
        resp.body = json.dumps({
            'id': 0,
            'sql': 'ok',
            'sql_duration': duration
        })
        resp.status = falcon.HTTP_OK


class Ping(object):

    def on_get(self, req: Request, resp: Response) -> None:
        build_information = BuildInformation.fetch()
        details = {
            'id': 0,
            'name': build_information.name(),
            'version': build_information.version(),
            'build_date': build_information.build_date(),
            'build_epoch_sec': build_information.build_date_epoch(),
            'environment': build_information.environment(),
            'repository': build_information.repository(),
        }
        resp.body = json.dumps(details)
        resp.status = falcon.HTTP_OK
