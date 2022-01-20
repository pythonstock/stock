#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import json
from tornado import gen
import libs.common as common
import libs.stock_web_dic as stock_web_dic
import web.base as webBase
import logging
import datetime



class newHomeHandler(webBase.BaseHandler):
    @gen.coroutine
    def get(self):
        self.render("new_index.html",
                    pythonStockVersion=common.__version__,
                    leftMenu=webBase.GetLeftMenu(self.request.uri))