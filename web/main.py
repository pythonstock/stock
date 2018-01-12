#!/usr/bin/python
# -*- coding: utf-8 -*-

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
import libs.common as common
import libs.stock_web_dic as stock_web_dic
import web.dataTableHandler as dataTableHandler
import web.chartHandler as chartHandler
import web.dataEditorHandler as dataEditorHandler
import web.dataIndicatorsHandler as dataIndicatorsHandler
import web.minstServingHandler as minstServingHandler
import web.base as webBase
import logging

# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            # 设置路由
            (r"/", HomeHandler),
            # 使用datatable 展示报表数据模块。
            (r"/stock/api_data", dataTableHandler.GetStockDataHandler),
            (r"/stock/data", dataTableHandler.GetStockHtmlHandler),
            # chart 数据图
            (r"/stock/chart", chartHandler.GetChartHtmlHandler),
            (r"/stock/chart/image1", chartHandler.ImageHandler),
            # 数据修改dataEditor。
            (r"/data/editor", dataEditorHandler.GetEditorHtmlHandler),
            (r"/data/editor/save", dataEditorHandler.SaveEditorHandler),
            # 获得股票指标数据。
            (r"/data/indicators", dataIndicatorsHandler.GetDataIndicatorsHandler),

            # 数据修改dataEditor。
            (r"/minst_serving", minstServingHandler.GetMinstServingHtmlHandler),
            (r"/minst_serving/prediction", minstServingHandler.GetPredictionDataHandler),
            (r"/minst_serving/prediction2", minstServingHandler.GetPrediction2DataHandler),
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
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
