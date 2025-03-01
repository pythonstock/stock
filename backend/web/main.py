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
import pandas as pd
import numpy as np
import akshare as ak
import bokeh as bh
import sqlalchemy
import json

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            # 设置路由
            (r"/", HomeHandler),
            (r"/stock/", HomeHandler),
            (r"/api/v1/package_verison", PackageVersionHandler),# 包版本
            (r"/api/v1/menu_list", MenuListHandler), # 菜单接口
            (r"/test_akshare", TestHandler),# 测试页面，做写js 测试。
            (r"/test2", Test2Handler),# 测试页面，做写js 测试。
            # 使用datatable 展示报表数据模块。
            (r"/api/v1/api_data", dataTableHandler.GetStockDataHandler),
            (r"/stock/data", dataTableHandler.GetStockHtmlHandler),
            # 数据修改dataEditor。
            (r"/data/editor", dataEditorHandler.GetEditorHtmlHandler),
            (r"/data/editor/save", dataEditorHandler.SaveEditorHandler),
            # 获得股票指标数据。
            (r"/api/v1/data/indicators", dataIndicatorsHandler.GetDataIndicatorsHandler),
        ]
        settings = dict(  # 配置
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,  # True,
            # cookie加密
            cookie_secret="027bb1b670eddf0392cdda8709268a17b58b7",
            debug=True,
            default_encoding="utf-8",
        )
        super(Application, self).__init__(handlers, **settings)
        # Have one global connection to the blog DB across all handlers
        self.db = torndb.Connection(
            charset="utf8", max_idle_time=3600, connect_timeout=1000,
            host=common.MYSQL_HOST, database=common.MYSQL_DB,
            user=common.MYSQL_USER, password=common.MYSQL_PWD)


# 获得包版本 handler。
class PackageVersionHandler(webBase.BaseHandler):
    @gen.coroutine
    def get(self):
        pandasVersion = pd.__version__
        numpyVersion = np.__version__
        sqlalchemyVersion = sqlalchemy.__version__
        akshareVersion = ak.__version__
        bokehVersion = bh.__version__
        # 返回包的版本信息。
        obj = {
            "code": 20000,
            "message": "success",
            "pandasVersion" : pandasVersion,
            "numpyVersion" : numpyVersion,
            "sqlalchemyVersion" : sqlalchemyVersion,
            "akshareVersion" : akshareVersion,
            "bokehVersion" : bokehVersion,
             "stockstatsVersion": "0.3.2"
        }
        # logging.info("####################")
        # logging.info(obj)
        self.write(json.dumps(obj))


# 获得菜单列表数据 handler。
class MenuListHandler(webBase.BaseHandler):
    @gen.coroutine
    def get(self):
        
        leftMenuList = stock_web_dic.STOCK_WEB_DATA_LIST
        out_data = []
        menu_name = ''
        menu_children = []
        index = 0
        for table_info in leftMenuList:
            print(table_info.name)
            index = index + 1
            # 使用 children 作为二级菜单。
            tmp_menu = {
                    "name": table_info.name,
                    "path": "/stock/table/" + table_info.table_name
            }
            menu_children.append(tmp_menu)

            # 使用 type作为 一级目录
            if menu_name != table_info.type or index == len(leftMenuList):
                # 进行数据循环
                if menu_name != '' :
                    if index != len(leftMenuList):
                        menu_children.pop() # 删除当前的节点信息。
                    tmp_children = list(menu_children)
                    tmp_menu2 = {
                        "name": menu_name,
                        "path": "#",
                        "children": tmp_children
                    }
                    # 下一个数据清空和放置。
                    menu_children = []
                    menu_children.append(tmp_menu)

                    out_data.append(tmp_menu2)
                menu_name = table_info.type
        
        obj = {
            "code": 20000,
            "message": "success",
            "data": out_data
        }
        print(out_data)
        # self.write(json.dumps(o
        self.write(json.dumps(obj))


# 首页handler。
class HomeHandler(webBase.BaseHandler):
    @gen.coroutine
    def get(self):
        print("################## index.html ##################")
        pandasVersion = pd.__version__
        numpyVersion = np.__version__
        akshareVersion = ak.__version__
        bokehVersion = bh.__version__
        #stockstatsVersion = ss.__version__ # 没有这个函数，但是好久不更新了
        # https://github.com/jealous/stockstats
        self.render("index.html", pandasVersion=pandasVersion, numpyVersion=numpyVersion,
                    akshareVersion=akshareVersion, bokehVersion=bokehVersion,
                    stockstatsVersion="0.3.2",
                    pythonStockVersion = common.__version__,
                    leftMenu=webBase.GetLeftMenu(self.request.uri))
class TestHandler(webBase.BaseHandler):
    @gen.coroutine
    def get(self):
        self.render("test_akshare.html", entries="hello",
                    pythonStockVersion=common.__version__,
                    leftMenu=webBase.GetLeftMenu(self.request.uri))
class Test2Handler(webBase.BaseHandler):
    @gen.coroutine
    def get(self):
        self.render("test2.html", entries="hello",
                    pythonStockVersion=common.__version__,
                    leftMenu=webBase.GetLeftMenu(self.request.uri))

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    port = 9090
    http_server.listen(port)
    # tornado.options.options.logging = "debug"
    tornado.options.parse_command_line()

    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
