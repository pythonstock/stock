#!/bin/sh


HAS_TF=`docker images tensorflow/tensorflow | wc -l `
if [ $HAS_TF -lt 2 ];then
    docker pull tensorflow/tensorflow:latest-devel
fi

HAS_TF_BASE=`docker images github.com/pythonstock/stock/tensorflow-py3 | wc -l `
if [ $HAS_TF_BASE -lt 2 ];then
    sh buildBase.sh
fi

HAS_TF_STOCK=`docker images github.com/pythonstock/stock/tensorflow-py3-stock | wc -l `
if [ $HAS_TF_STOCK -lt 2 ];then
    sh buildStock.sh
fi

DB_IS_RUN=`docker ps --filter "name=mariadb" --filter "status=running" | wc -l `
if [ $DB_IS_RUN -lt 2 ]; then
    sh startMysql.sh
fi

#检查stock启动
STOCK_IS_RUN=`docker ps --filter "name=stock" --filter "status=running" | wc -l `
if [ $STOCK_IS_RUN -ge 2 ]; then
    echo "stop & rm stock ..."
    docker stop stock && docker rm stock
fi

sleep 1

echo "starting stock ..."
# /data/stock 是代码目录 -v /data/stock:/data/stock 是开发模式。
docker run -itd --link=mariadb --name stock  \
    -p 8888:8888 \
    -p 6006:6006 \
    -p 9999:9999 \
    -p 8500:8500 \
   github.com/pythonstock/stock/tensorflow-py3-stock:latest
