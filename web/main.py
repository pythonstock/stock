#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import bcrypt
import concurrent.futures
import MySQLdb
import markdown
import os.path
import json
import subprocess
import torndb
import tornado.escape
from tornado import gen
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import libs.common as common

# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/api/stock/get_data", GetStockDataHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            # RANDOM_VALUE
            cookie_secret="fc03ad14f21cf81867cbed33109027bb1b670eddf0392cdda8709268a17b58b7",
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)
        # Have one global connection to the blog DB across all handlers
        self.db = torndb.Connection(
            host=common.MYSQL_HOST, database=common.MYSQL_DB,
            user=common.MYSQL_USER, password=common.MYSQL_PWD)


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class HomeHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        self.render("index.html", entries="hello")

# 获得股票数据内容。
class GetStockDataHandler(BaseHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json;charset=UTF-8')

        print(self.request.arguments.items())

        param_length = self.get_argument("length", default=None, strip=False)
        print("param_length:",param_length)
        param_columns = self.get_arguments("columns")
        print("get param_columns:",param_columns)
        array = []
        for j in range(0, 100):
            array.append([
                "Charde",
                "Marshall",
                "Regional Director",
                "San Francisco",
                "16th Oct 08",
                "$470,600" + str(j)
            ])
        obj = {
            "draw": 0,
            "recordsTotal": 20,
            "recordsFiltered": 20,
            "data": array
        }
        self.write(json.dumps(obj))


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    port = 9999
    http_server.listen(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
