import sys
import logging
from flask import Flask, Response, request, send_file
from multiprocessing import Process

cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


# return the requested file
class EndpointAction(object):
    def __call__(self, file):
        return send_file(file)


class RESTServer(object):
    app = None

    def __init__(self, port, endpoint='/<file>', endpoint_name='download file endpoint'):
        self.port = int(port)
        self.app = Flask("file-server")
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction())
        self.server_process = Process(target=self.async_run)

    # start the flask server on separate thread
    def async_run(self):
        self.app.run(port=self.port)

    def run(self):
        self.server_process.start()

    def terminate(self):
        self.server_process.terminate()
