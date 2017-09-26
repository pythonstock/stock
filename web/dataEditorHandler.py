#!/usr/local/bin/python
# -*- coding: utf-8 -*-


from tornado import gen
import libs.stock_web_dic as stock_web_dic
import web.base as webBase
import logging
import tornado.web
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io

def GenImage(freq):
    t = np.linspace(0, 10, 500)
    y = np.sin(t * freq * 2 * 3.141)
    fig1 = plt.figure()
    plt.plot(t, y)
    plt.xlabel('Time [s]')
    memdata = io.BytesIO()
    plt.grid(True)
    plt.savefig(memdata, format='png')
    image = memdata.getvalue()
    return image


class ImageHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        image = GenImage(0.5)
        self.set_header('Content-type', 'image/png')
        self.set_header('Content-length', len(image))
        self.write(image)

# 获得页面数据。
class GetEditorHtmlHandler(webBase.BaseHandler):
    @gen.coroutine
    def get(self):
        name = self.get_argument("name", default=None, strip=False)
        stockWeb = stock_web_dic.STOCK_WEB_DATA_MAP[name]
        # self.uri_ = ("self.request.url:", self.request.uri)
        # print self.uri_
        self.render("data_editor.html", stockWeb=stockWeb, leftMenu=webBase.GetLeftMenu(self.request.uri))


# 获得页面数据。
class SaveEditorHandler(webBase.BaseHandler):
    @gen.coroutine
    def post(self):
        action = self.get_argument("action", default=None, strip=False)
        logging.info(action)

        # 支持多排序。使用shift+鼠标左键。
        for item, val in self.request.arguments.items():
            logging.info("item: %s, val: %s" % (item, val) )
        #stockWeb = data_editor_dic.DATA_EDITOR_MAP[name]
        # self.uri_ = ("self.request.url:", self.request.uri)
        # print self.uri_
        if action == "create" :
            logging.info("create")

        elif action == "edit":
            logging.info("edit")

        elif action == "remove":
            logging.info("remove")

        self.write("{\"data\":[{}]}")