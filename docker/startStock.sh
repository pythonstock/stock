#!/bin/sh

# /data/stock 是代码目录 -v /data/stock:/data/stock 是开发模式。
docker run -itd --link=mariadb  \
        -p 8888:8888 \
        -p 6006:6006 \
        -p 9999:9999 \
       github.com/pythonstock/stock/tensorflow-py3-stock:latest