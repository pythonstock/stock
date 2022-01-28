#!/bin/bash

PWD=`pwd`

#检查vnpy启动
VNPY_IS_RUN=`docker ps --filter "name=vnpy" --filter "status=running" | wc -l `
if [ $VNPY_IS_RUN -ge 2 ]; then
	echo "stop & rm vnpy ..."
	docker stop vnpy && docker rm vnpy
fi

sleep 1

echo "starting vnpy ..."
#映射本地代码。

echo "#############  run dev ############# "
docker run -itd --name vnpy  \
	--net=host --env="DISPLAY" \
	-e LANG=zh_CN.GB18030 -e LC_CTYPE=zh_CN.GB18030 -e PYTHONIOENCODING=utf-8 \
	-p 8888:8888 -p 8000:8000 --restart=always \
	-v $(realpath ~/.Xauthority):/root/.Xauthority \
	-v ${PWD}/../../../vnpy:/data/vnpy \
	-v ${PWD}/../data/logs:/data/logs \
	gao9/vnpy:latest
exit 1;


