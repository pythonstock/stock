#!/usr/local/bin/python3
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
import numpy as np
from PIL import Image
from PIL import ImageOps
import base64
import io #python2 import StringIO

work_dir = "/data/stock/tf/minst_serving/input_data"
out_dir = "/static/img/minst_serving/%s.bmp"


# 获得页面数据。
class GetMinstServingHtmlHandler(webBase.BaseHandler):
    @gen.coroutine
    def get(self):
        # print self.uri_
        arr = np.arange(30)
        image_array = []
        for idx in arr:
            out_file = out_dir % ("%05d" % idx)
            print(out_file)
            image_array.append(out_file)
        self.render("minst_serving.html", image_array=image_array)


# 获得股票数据内容。
class GetPredictionDataHandler(webBase.BaseHandler):
    def get(self):
        # 获得分页参数。
        img_url = self.get_argument("img_url", default=0, strip=False)
        print(img_url)
        img_obj = Image.open("/data/stock/web" + img_url)
        print("img_obj", img_obj)
        server = "0.0.0.0:8500"
        prediction = do_inference(server, img_obj)
        print('######### prediction : ', prediction)
        self.write(json.dumps(prediction))


# 获得股票数据内容。
class GetPrediction2DataHandler(webBase.BaseHandler):
    def post(self):
        # 获得分页参数。
        imgStr = self.get_argument("txt", default="", strip=False)
        # imgStr.replace(" ", "+")
        imgStr = base64.b64decode(imgStr)
        print("imgStr:", type(imgStr))
        image = Image.open(io.StringIO(imgStr))
        image.thumbnail((28, 28), Image.ANTIALIAS)
        image = image.convert('L')
        image = ImageOps.invert(image)
        image.save(work_dir + "/web-tmp.bmp", format="BMP") #保存看看，是否
        #print(image)
        # img_url = self.get_argument("img_url", default=0, strip=False)
        # print(img_url)
        server = "0.0.0.0:8500"
        prediction = do_inference(server, image)
        print('######### prediction : ', prediction)
        self.write(json.dumps(prediction))



# 调用 grpc 代码，将图片转换成数组，让后放到 grpc 调用。
def do_inference(hostport, img_obj):

    print("############", hostport)

