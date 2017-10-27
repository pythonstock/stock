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
        server = "127.0.0.1:8500"
        prediction = do_inference(server, img_url)
        print('######### prediction : ', prediction)
        self.write(json.dumps(prediction))


import sys

from grpc.beta import implementations
import numpy
import tensorflow as tf

from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2
import threading


class _ResultCounter(object):
    """Counter for the prediction results."""

    def __init__(self, num_tests, concurrency):
        self._num_tests = num_tests
        self._concurrency = concurrency
        self._result = 0
        self._done = 0
        self._active = 0
        self._condition = threading.Condition()

    def set_result(self, result):
        with self._condition:
            self._done += 1
            self._result = result

    def dec_active(self):
        with self._condition:
            self._active -= 1
            self._condition.notify()

    def get_error_rate(self):
        with self._condition:
            while self._done != self._num_tests:
                self._condition.wait()
            return self._result

    def throttle(self):
        with self._condition:
            while self._active == self._concurrency:
                self._condition.wait()
            self._active += 1


def _create_rpc_callback(label, result_counter):
    """Creates RPC callback function.

    Args:
      label: The correct label for the predicted example.
      result_counter: Counter for the prediction result.
    Returns:
      The callback function.
    """

    def _callback(result_future):
        """Callback function.

        Calculates the statistics for the prediction result.

        Args:
          result_future: Result future of the RPC.
        """
        exception = result_future.exception()
        if exception:
            print(exception)
        else:
            sys.stdout.write('.')
            sys.stdout.flush()
            response = numpy.array(
                result_future.result().outputs['scores'].float_val)
            # print("response:\n",result_future.result())
            result = numpy.argmax(response)  # 返回prediction。
            result_counter.set_result(result)
            print("response:\n", result_future.result())
            print("prediction:\n", result)
        result_counter.dec_active()

    return _callback


# 调用 grpc 代码，将图片转换成数组，让后放到 grpc 调用。
def do_inference(hostport, img_file):
    host, port = hostport.split(':')
    print(host, port)

    # 创建 python grpc 代码调用。
    channel = implementations.insecure_channel(host, int(port))
    stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
    request = predict_pb2.PredictRequest()
    request.model_spec.name = 'mnist'
    request.model_spec.signature_name = 'predict_images'
    # image, label = test_data_set.next_batch(1)
    label = np.array([1], dtype=np.uint8)

    result_counter = _ResultCounter(1, 1)
    img = Image.open("/data/stock/web" + img_file)

    img_array = np.array(img, dtype=np.float32)
    img_array = img_array.reshape(img_array.size)

    # 新方法。很接近原始数据。
    img_new_arr = np.divide(np.mod(img_array, 255), 255.0)
    # img_new_arr = np.divide(np.subtract(255.0, img_array), 255.0)
    # print(img_new_arr)

    print("############", type(img_new_arr[0]))
    print("############", type(label[0]))
    result_counter.throttle()
    print("############ throttle ")
    request.inputs['images'].CopyFrom(
        tf.contrib.util.make_tensor_proto(img_new_arr, shape=[1, img_new_arr.size]))
    result_future = stub.Predict.future(request, 5.0)  # 5 seconds
    result_future.add_done_callback(
        _create_rpc_callback(label[0], result_counter))
    print("############")
    return result_counter.get_error_rate()
