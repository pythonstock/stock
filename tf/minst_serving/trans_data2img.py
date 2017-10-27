#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
import mnist_input_data
import numpy as np

input_dir = "/data/stock/tf/minst_serving/input_data"
out_dir = "/data/stock/web/static/img/minst_serving/%s.bmp"


# https://pillow.readthedocs.io/en/3.0.0/reference/Image.html
def trans_image(idx, img_arr):
    # https://docs.scipy.org/doc/numpy/reference/routines.math.html
    img_arr = np.add(np.multiply(255.0, img_arr), 255.0)
    img_arr = np.array(img_arr, dtype=np.uint8)  # 转换成0-255的区间数据
    img_arr = img_arr.reshape(28, 28)  # 转换成28*28的灰度图形。
    # print(img_arr)
    # imgplot = plt.imshow(img, cmap='gray') #显示灰度图像
    img_1 = Image.fromarray(img_arr)
    out_file = out_dir % idx
    # 必须是BMP的类型，其他类型，数据都经过压缩。造成数据不一致。
    img_1.save(out_file, format="BMP")
    return img_arr


def read_image_arr(image_file):
    img = Image.open(image_file)

    img_array = np.array(img, dtype=np.uint8)
    # print(img_array)
    img_array = img_array.reshape(img_array.size)
    img_array = np.divide(np.mod(img_array, 255), 255.0)
    #img_array = np.divide(np.subtract(255.0, img_array), 255.0)
    # print(img_array)
    return img_array


if __name__ == '__main__':

    test_data_set = mnist_input_data.read_data_sets(input_dir).test
    num_tests = 1
    for idx in range(num_tests):
        image, label = test_data_set.next_batch(1)
        # print(image[0])
        # arr = np.asanyarray(image[0]).reshape(28, 28)
        # print(arr)
        print("############", type(image[0][0]))
        print("############", label[0])
        idx_num = "%05d" % int(idx)
        img_1 = trans_image(idx_num, image)

        # print(image[0])
        out_file = out_dir % idx_num
        img_2 = read_image_arr(out_file)
        print("############")
        # print(img_2)
        img_1 = np.array(image[0]).reshape(28, 28)
        img_2 = np.array(img_2).reshape(28, 28)
        print("############")
        print(img_1[16])
        print("############")
        print(img_2[16])
        is_equal = np.array_equal(image[0], img_2)
        print("img save is equal img read :", is_equal)
