#!/usr/bin/python3
# -*- coding: utf-8 -*-

from tornado import gen
import web.base as webBase
import logging

# 首映 bokeh 画图。
from bokeh.plotting import figure
from bokeh.embed import components


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

        comp_list = []
        # prepare some data
        x = [1, 2, 3, 4, 5]
        y = [6, 7, 2, 4, 5]

        # create a new plot with a title and axis labels
        p = figure(
            plot_width=400, plot_height=300,
            title="simple line example",
            x_axis_label='x', y_axis_label='y'
        )

        # add a line renderer with legend and line thickness
        p.line(x, y, legend="Temp.", line_width=2)

        comp1 = components(p)
        comp2 = components(p)
        comp_list.append(comp1)
        comp_list.append(comp2)

        self.render("stock_indicators.html", comp_list=comp_list, leftMenu=webBase.GetLeftMenu(self.request.uri))
