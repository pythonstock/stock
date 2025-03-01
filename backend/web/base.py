#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import tornado.web
import libs.stock_web_dic as stock_web_dic
import libs.common as common
import logging

#基础handler，主要负责检查mysql的数据库链接。
class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        headers = self.request.headers
        # logging.info('head的类型：',type(headers))
        origin =  headers.get('origin',None)
        logging.info("######################## BaseHandler ########################")
        logging.info(origin)
        
        if origin != None and origin.find("localhost") > 0:
            self.set_header("Access-Control-Allow-Credentials", "true")
            self.set_header("Access-Control-Allow-Origin",origin)
            self.set_header("Access-Control-Allow-Methods", "POST, GET, PUT, DELETE, OPTIONS")
            self.set_header("Access-Control-Allow-Headers", "x-token, authorization, Authorization, Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods")
            self.set_header("Access-Control-Expose-Headers", "Cache-Control, Content-Language, Content-Type, Expires, Last-Modified, Pragma")
    # 同时定义一个option方法
    def options(self):
        self.set_status(204)
        self.finish()

    @property
    def db(self):
        try:
            # check every time。
            self.application.db.query("SELECT 1 ")
        except Exception as e:
            print(e)
            self.application.db.reconnect()
        return self.application.db

class LeftMenu:
    def __init__(self, url):
        self.leftMenuList = stock_web_dic.STOCK_WEB_DATA_LIST
        self.current_url = url

# 获得左菜单。
def GetLeftMenu(url):
    return LeftMenu(url)
