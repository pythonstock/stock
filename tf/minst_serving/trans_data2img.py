#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
import mnist_input_data
import numpy as np

input_dir = "/data/stock/tf/minst_serving/input_data"
out_dir = "/data/stock/web/static/img/minst_serving/%s.jpeg"


def trans_image(idx, img_arr):
    # https://docs.scipy.org/doc/numpy/reference/routines.math.html
    img_arr = np.add(np.multiply(255.0, img_arr), 255.0)
    img_arr = np.array(img_arr, dtype=np.uint8)  # 转换成0-255的区间数据
    img_arr = img_arr.reshape(28, 28)  # 转换成28*28的灰度图形。
    # print(img_arr)
    # imgplot = plt.imshow(img, cmap='gray') #显示灰度图像
    img_1 = Image.fromarray(img_arr)
    out_file = out_dir % idx
    img_1.save(out_file)


if __name__ == '__main__':

    test_data_set = mnist_input_data.read_data_sets(input_dir).test
    num_tests = 20
    for idx in range(num_tests):
        image, label = test_data_set.next_batch(1)
        idx_num = "%05d" % int(idx)
        trans_image(idx_num, image)
        print("############", idx_num, label)
