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
from send import send
from utility import predict
from io import BytesIO
from google.cloud import firestore
import base64
# import firebase_admin
# from firebase_admin import credentials

import numpy as np
from PIL import Image


define("port", default=9000, help="runs on the given port", type=int)


class MyAppException(tornado.web.HTTPError):
    pass


class BaseHandler(tornado.web.RequestHandler):

    def db(self):
        clientz = self.settings['db_client']
        db = clientz.projectx
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


class MLHandler(BaseHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Content-type', 'application/json')

    @coroutine
    def post(self):
        file_body = self.request.files['pic'][0]['body']
        img = Image.open(BytesIO(file_body))
        img.save("current.jpg")
        img = np.array(img).astype('uint8')
        ml_response = yield predict.predict(img)


        gp = self.get_body_argument("gps")
        print(ml_response)




        # db = self.db()
        # details = yield db.find_one({"District": "Vellore"})
        # if int(send(details=details)) != 201:
        #     self.write(json.dumps({"status": "something went wrong"}))
        #
        # if not ml_response:
        #     if int(send()) != 201:
        #         self.write(json.dumps({"status": "something went wrong"}))
        fire = firestore.Client()
        x = fire.collection("data").document("1")
        with open("current.jpg", "rb") as f:
            ig = base64.b64encode(f.read())
            payload = {
                "gps": gp,
                "label": ml_response['img_label'],
                "img": ig
            }
            y = x.get().to_dict()['data']
            y.append(payload)
            x.set({"data": y})

        self.write(json.dumps({'flag': 'Everthing is coool'}))


if __name__ == "__main__":
    options.parse_command_line()
    client = motor_tornado.MotorClient("mongodb://user:pass@ds143030.mlab.com:43030/projectx")
    app = tornado.web.Application(
        handlers=[
            (r"/mlpredict", MLHandler)
        ],
        default_handler_class=my404handler,
        debug=True,
        db_client=client
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(os.environ.get("PORT", options.port))
    tornado.ioloop.IOLoop.instance().start()
