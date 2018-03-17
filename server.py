import json
import os
import traceback
import tornado.httpserver
import tornado.ioloop
import tornado.web
from motor import motor_tornado
from tornado.gen import coroutine
from tornado.options import define, options
from models import users, patient
from passlib.hash import pbkdf2_sha256
import tornado.escape
import jwt
from functools import wraps
from oauth2client import client as auth_client
from oauth2client import crypt
from io import BytesIO
from PIL import Image
import base64
import requests

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
        img = Image.open(BytesIO(file_body))
        img.save("current.jpg")
        f = open("current.jpg", "rb")
        images = [{'content': base64.b64encode(f.read()).decode('UTF-8')}]
        x = requests.post("https://skindoc-10ef5.appspot.com/melanoma/predict", json=images)
        f.close()
        self.write(json.dumps(x.json()[0]))


if __name__ == "__main__":
    options.parse_command_line()
    client = motor_tornado.MotorClient("mongodb://"+os.environ['tornado_user']+":"+ os.environ['tornado_pass']
                                       +"@ds117605.mlab.com:17605/tornado")
    app = tornado.web.Application(
        handlers=[
            (r"/mlpredict", MLHandler)
        ],
        default_handler_class = my404handler,
        debug = True,
        cookie_secret = os.environ['cookie_secret'],
        login_url = "/login",
        db_client = client,
        ap_details = dict(),
        client_id = os.environ['sk_client'],
        template_path=os.path.join(os.path.dirname(__file__), "template"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(os.environ.get("PORT", options.port))
    tornado.ioloop.IOLoop.instance().start()