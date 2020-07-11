#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import os.path
import torndb
import tornado.escape
from tornado import gen
import tornado.httpserver
import tornado.ioloop
import tornado.options
import libs.common as common
import libs.stock_web_dic as stock_web_dic
import web.dataTableHandler as dataTableHandler
import web.dataEditorHandler as dataEditorHandler
import web.dataIndicatorsHandler as dataIndicatorsHandler
import web.base as webBase

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            # 设置路由
            (r"/", HomeHandler),
            # 使用datatable 展示报表数据模块。
            (r"/stock/api_data", dataTableHandler.GetStockDataHandler),
            (r"/stock/data", dataTableHandler.GetStockHtmlHandler),
            # 数据修改dataEditor。
            (r"/data/editor", dataEditorHandler.GetEditorHtmlHandler),
            (r"/data/editor/save", dataEditorHandler.SaveEditorHandler),
            # 获得股票指标数据。
            (r"/data/indicators", dataIndicatorsHandler.GetDataIndicatorsHandler),
        ]
        settings = dict(  # 配置
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,  # True,
            # cookie加密
            cookie_secret="027bb1b670eddf0392cdda8709268a17b58b7",
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)
        # Have one global connection to the blog DB across all handlers
        self.db = torndb.Connection(
            charset="utf8", max_idle_time=3600, connect_timeout=1000,
            host=common.MYSQL_HOST, database=common.MYSQL_DB,
            user=common.MYSQL_USER, password=common.MYSQL_PWD)


# 首页handler。
class HomeHandler(webBase.BaseHandler):
    @gen.coroutine
    def get(self):
        self.render("index.html", entries="hello", leftMenu=webBase.GetLeftMenu(self.request.uri))


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    port = 9999
    http_server.listen(port)
    # tornado.options.options.logging = "debug"
    tornado.options.parse_command_line()

    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
