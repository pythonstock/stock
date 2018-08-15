#!/usr/local/bin/python3
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
class GetChartHtmlHandler(webBase.BaseHandler):
    @gen.coroutine
    def get(self):
        name = self.get_argument("table_name", default=None, strip=False)
        #stockWeb = stock_web_dic.STOCK_WEB_DATA_MAP[name]
        # self.uri_ = ("self.request.url:", self.request.uri)
        # print self.uri_
        logging.info("chart...")
        self.render("stock_chart.html", entries="", leftMenu=webBase.GetLeftMenu(self.request.uri))

