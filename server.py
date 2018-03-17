import json
import os
import traceback
import tornado.httpserver
import tornado.ioloop
import tornado.web
from motor import motor_tornado
from tornado.gen import coroutine
from tornado.options import define, options
import tornado.escape
import base64
import requests
from send import send

define("port", default=8080, help="runs on the given port", type=int)


class MyAppException(tornado.web.HTTPError):
    pass


class BaseHandler(tornado.web.RequestHandler):

    def db(self):
        clientz = self.settings['db_client']
        db = clientz.tornado
        return db

    def write_error(self, status_code, **kwargs):
        self.set_header('Content-Type', 'application/json')
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            lines = []
            for line in traceback.format_exception(*kwargs["exc_info"]):
                lines.append(line)
            self.write(json.dumps({
                        'status_code': status_code,
                        'message': self._reason,
                        'traceback': lines,
                }))
        else:
            self.write(json.dumps({
                    'status_code': status_code,
                    'message': self._reason,
                }))


class my404handler(BaseHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps({
                'status_code': 404,
                'message': 'illegal call.'
        }))


class MLHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Content-type', 'application/json')

    @coroutine
    def post(self):
        file_body = self.request.files['filefieldname'][0]['body']
        ml_response = False
        details = {}
        if send(details=details) != 201:
            self.write(json.dumps({"status": "something went wrong"}))

        if not ml_response:
            if send() != 201:
                self.write(json.dumps({"status": "something went wrong"}))
                
        self.write(json.dumps({"status": "success"}))


if __name__ == "__main__":
    options.parse_command_line()
    client = motor_tornado.MotorClient("mongodb://"+os.environ['tornado_user']+":"+ os.environ['tornado_pass']
                                       +"@ds117605.mlab.com:17605/tornado")
    app = tornado.web.Application(
        handlers=[
            (r"/mlpredict", MLHandler)
        ],
        default_handler_class = my404handler,
        debug=True,
        db_client=client
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(os.environ.get("PORT", options.port))
    tornado.ioloop.IOLoop.instance().start()
