#!/usr/bin/python3
# -*- coding: utf-8 -*-

from tornado import gen
import web.base as webBase
import logging


# 获得页面数据。
class GetDataIndicatorsHandler(webBase.BaseHandler):
    @gen.coroutine
    def get(self):
        code = self.get_argument("code", default=None, strip=False)
        print(code)
        # self.uri_ = ("self.request.url:", self.request.uri)
        # print self.uri_
        try:
            print("#######")
        except Exception as e:
            print("error :", e)
        logging.info("####################GetStockHtmlHandlerEnd")
        self.render("stock_indicators.html", leftMenu=webBase.GetLeftMenu(self.request.uri))
