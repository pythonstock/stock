#!/bin/bash

PWD=`pwd`



#检查stock启动
STOCK_IS_RUN=`docker ps --filter "name=vnpy" --filter "status=running" | wc -l `
if [ $STOCK_IS_RUN -ge 2 ]; then
	echo "stop & rm vnpy ..."
	docker stop vnpy && docker rm vnpy
fi

sleep 1

echo "starting vnpy ..."
# 1 是开发环境。映射本地代码。
if [ $# == 1 ] ; then
    echo "#############  run dev ############# "
    # /data/stock 是代码目录 -v /data/stock:/data/stock 是开发模式。
    mkdir -p notebooks

    docker run -itd --name vnpy  \
		--net=host --env="DISPLAY" \
		-e LANG=zh_CN.UTF-8 -e LC_CTYPE=zh_CN.UTF-8 -e PYTHONIOENCODING=utf-8 \
		-p 9001:9001 \
		-p 8888:8888 -p 9999:9999 --restart=always \
		-v ${PWD}/../data/logs:/data/logs \
		gao/vnpy:v1
    exit 1;
else
    echo "############# run online ############# "
    # /data/stock 是代码目录 -v /data/stock:/data/stock 是开发模式。
    docker run -itd --link=mysqldb --name vnpy  \
      -p 9001:9001 \
      -p 8888:8888 -p 9999:9999 --restart=always \
       gao/vnpy:2022-01
    exit 1;
fi

