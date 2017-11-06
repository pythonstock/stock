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
import numpy as np
from PIL import Image
from PIL import ImageOps
import base64
import StringIO

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
        image = Image.open(StringIO.StringIO(imgStr))
        image.thumbnail((28, 28), Image.ANTIALIAS)
        image = image.convert('L')
        #image = ImageOps.invert(image)
        image.save(work_dir + "/web-tmp.bmp", format="BMP") #保存看看，是否
        #print(image)
        # img_url = self.get_argument("img_url", default=0, strip=False)
        # print(img_url)
        server = "0.0.0.0:8500"
        prediction = do_inference(server, image)
        print('######### prediction : ', prediction)
        self.write(json.dumps(prediction))


import sys

from grpc.beta import implementations
import numpy
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2
import threading

hostport = "0.0.0.0:8500"
host, port = hostport.split(':')
print(host, port)

# 创建 python grpc 代码调用。全局变量。不能每次都创建。
channel = implementations.insecure_channel(host, int(port))
stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)


# 调用 grpc 代码，将图片转换成数组，让后放到 grpc 调用。
def do_inference(hostport, img_obj):
    request = predict_pb2.PredictRequest()
    request.model_spec.name = 'mnist'
    request.model_spec.signature_name = 'predict_images'
    # image, label = test_data_set.next_batch(1)
    label = np.array([1], dtype=np.uint8)

    img_array = np.array(img_obj, dtype=np.float32)
    img_array = img_array.reshape(img_array.size)

    # 新方法。很接近原始数据。
    img_new_arr = np.divide(img_array, 255.0)
    # img_new_arr = np.divide(np.subtract(255.0, img_array), 255.0)
    # print(img_new_arr)

    print("############", type(img_new_arr[0]))
    print("############", type(label[0]))
    print("############ throttle ")
    # result_counter.throttle()
    request.inputs['images'].CopyFrom(
        tf.contrib.util.make_tensor_proto(img_new_arr, shape=[1, img_new_arr.size]))
    result_future = stub.Predict.future(request, 1.0)  # 5 seconds

    prediction = ""
    exception = result_future.exception()
    if exception:
        prediction = str(exception)
        print(exception)
    else:
        sys.stdout.write('.')
        sys.stdout.flush()
        response = numpy.array(
            result_future.result().outputs['scores'].float_val)
        # print("response:\n",result_future.result())
        prediction = str(numpy.argmax(response))
    print("############", prediction)
    return prediction
