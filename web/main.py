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
import libs.stock_web_dic as stock_web_dic

# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [  # 设置路由
            (r"/", HomeHandler),
            (r"/stock/api_data", GetStockDataHandler),
            (r"/stock/data", GetStockHtmlHandler),
        ]
        settings = dict(  # 配置
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            # cookie加密
            cookie_secret="027bb1b670eddf0392cdda8709268a17b58b7",
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
        try:
            # check every time。
            self.application.db.query("SELECT 1 ")
        except Exception as e:
            print(e)
            self.application.db.reconnect()
        return self.application.db


class HomeHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        self.render("index.html", entries="hello", leftMenu=getLeftMenu(self.request.uri))


class LeftMenu:
    def __init__(self, url):
        self.leftMenuList = stock_web_dic.STOCK_WEB_DATA_LIST
        self.current_url = url


# 获得左菜单。
def getLeftMenu(url):
    return LeftMenu(url)


# 获得页面数据。
class GetStockHtmlHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        name = self.get_argument("name", default=None, strip=False)
        stockWeb = stock_web_dic.STOCK_WEB_DATA_MAP[name]
        # self.uri_ = ("self.request.url:", self.request.uri)
        # print self.uri_
        self.render("stock_web.html", stockWeb=stockWeb, leftMenu=getLeftMenu(self.request.uri))


# 获得股票数据内容。
class GetStockDataHandler(BaseHandler):
    def get(self):
        # https://datatables.net/manual/server-side
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        order_by_column = []
        order_by_dir = []
        # 支持多排序。使用shift+鼠标左键。
        for item, val in self.request.arguments.items():
            # print("order:", item)
            if str(item).startswith("order["):
                print("order:", item, ",val:", val[0])
            if str(item).startswith("order[") and str(item).endswith("[column]"):
                order_by_column.append(int(val[0]))
            if str(item).startswith("order[") and str(item).endswith("[dir]"):
                order_by_dir.append(val[0].decode("utf-8"))  # bytes转换字符串

        # 获得分页参数。
        start_param = self.get_argument("start", default=0, strip=False)
        length_param = self.get_argument("length", default=10, strip=False)
        print("page param:", length_param, start_param)

        name_param = self.get_argument("name", default=None, strip=False)
        stock_web = stock_web_dic.STOCK_WEB_DATA_MAP[name_param]

        # print("stockWeb :", stock_web)
        order_by_sql = ""
        # 增加排序。
        if len(order_by_column) != 0 and len(order_by_dir) != 0:
            order_by_sql = "  ORDER BY "
            idx = 0
            for key in order_by_column:
                # 找到排序字段和dir。
                col_tmp = stock_web.columns[key]
                dir_tmp = order_by_dir[idx]
                if idx != 0:
                    order_by_sql += " ,%s %s" % (col_tmp, dir_tmp)
                else:
                    order_by_sql += " %s %s" % (col_tmp, dir_tmp)
                idx += 1
        # 查询数据库。
        sql = " SELECT * FROM %s %s LIMIT %s,%s " % (stock_web.table_name, order_by_sql, start_param, length_param)
        print("select sql :", sql)
        stock_web_list = self.db.query(sql)
        stock_web_size = self.db.query(" SELECT count(1) as num FROM " + stock_web.table_name)
        print("stockWebList size :", stock_web_size)

        obj = {
            "draw": 0,
            "recordsTotal": stock_web_size[0]["num"],
            "recordsFiltered": stock_web_size[0]["num"],
            "data": stock_web_list
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
