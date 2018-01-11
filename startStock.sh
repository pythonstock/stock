#!/bin/sh

#检查stock启动
STOCK_IS_RUN=`docker ps --filter "name=pythonstock" --filter "status=running" | wc -l `
if [ $STOCK_IS_RUN -ge 2 ]; then
    echo "stop & rm pythonstock ..."
    docker stop pythonstock && docker rm pythonstock
fi

sleep 1

echo "starting pythonstock ..."
# /data/stock 是代码目录 -v /data/stock:/data/stock 是开发模式。
docker run -itd --name pythonstock  \
    -p 8888:8888 \
    -p 6006:6006 \
    -p 9999:9999 \
    -p 8500:8500 \
   pythonstock/pythonstock:latest
