from prometheus_client import CollectorRegistry, Counter, Histogram, generate_latest
import time
from falcon import Request, Response


class PrometheusMiddleware(object):
    def __init__(self, register: CollectorRegistry):
        self.registry = register
        self.requests = Counter(
            'http_total_request',
            'Counter of total HTTP requests',
            ['method', 'path', 'status'],
            registry=self.registry)

        self.request_histogram = Histogram(
            'request_latency_seconds',
            'Histogram of request latency',
            ['method', 'path', 'status'],
            registry=self.registry)
    
    def process_request(self, req: Request, resp: Response) -> None:
        req.start_time = time.time()

    def process_response(self, req: Request, resp: Response, resource, req_succeeded: bool) -> None:
        resp_time = time.time() - req.start_time

        self.requests.labels(method=req.method, path=req.path, status=resp.status).inc()
        self.request_histogram.labels(method=req.method, path=req.path, status=resp.status).observe(resp_time)

    def on_get(self, req: Request, resp: Response) -> None:
        data = generate_latest(self.registry)
        resp.content_type = 'text/plain; version=0.0.4; charset=utf-8'
        resp.body = str(data.decode('utf-8'))
