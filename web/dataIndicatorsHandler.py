#!/usr/local/bin/python
# -*- coding: utf-8 -*-

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
import libs.stock_web_dic as stock_web_dic
import web.base as webBase
import logging


# 获得页面数据。
class GetDataIndicatorsHandler(webBase.BaseHandler):
    @gen.coroutine
    def get(self):
        name = self.get_argument("table_name", default=None, strip=False)
        stockWeb = stock_web_dic.STOCK_WEB_DATA_MAP[name]
        # self.uri_ = ("self.request.url:", self.request.uri)
        # print self.uri_
        try:
            # 增加columns 字段中的【东方财富】
            tmp_idx = stockWeb.column_names.index("东方财富")
            logging.info(tmp_idx)
            try:
                # 防止重复插入数据。可能会报错。
                stockWeb.columns.remove("eastmoney_url")
            except Exception as e:
                print("error :", e)
            stockWeb.columns.insert(tmp_idx, "eastmoney_url")
        except Exception as e:
            print("error :", e)
        logging.info("####################GetStockHtmlHandlerEnd")
        self.render("stock_indicators.html", stockWeb=stockWeb, leftMenu=webBase.GetLeftMenu(self.request.uri))

