#!/usr/local/bin/python
# -*- coding: utf-8 -*-

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
import web.base as webBase
import logging


# 获得页面数据。
class GetMinstServingHtmlHandler(webBase.BaseHandler):
    @gen.coroutine
    def get(self):
        # print self.uri_
        self.render("minst_serving.html")


# 获得股票数据内容。
class GetPredictionDataHandler(webBase.BaseHandler):
    def get(self):
        # 获得分页参数。
        start_param = self.get_argument("start", default=0, strip=False)
        print(start_param)
