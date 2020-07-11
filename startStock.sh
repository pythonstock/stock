#!/bin/bash

DB_IS_RUN=`docker ps --filter "name=mariadb" --filter "status=running" | wc -l `
if [ $DB_IS_RUN -lt 2 ]; then

    #判断文件夹存在不。
    if [ ! -d "/data/mariadb/data" ]; then
        mkdir -p /data/mariadb/data
    fi

    HAS_DB=`docker images mariadb | wc -l `
    if [ $HAS_DB -ne 2 ];then
        docker pull mariadb
    fi

    ####################### 启动数据库 #######################
    #检查mariadb是否启动
    DB_IS_RUN=`docker ps --filter "name=mariadb" --filter "status=running" | wc -l `

    if [ $DB_IS_RUN -ne 2 ]; then
        docker run --name mariadb -v /data/mariadb/data:/var/lib/mysql --restart=always \
        -e MYSQL_ROOT_PASSWORD=mariadb -p 3306:3306 -d mariadb:latest
        echo "starting mariadb ..."
    else
        echo "mariadb is running !!!"
    fi

    ####################### 创建数据库 #######################
    echo "wait 10 second , and create stock database ."
    sleep 10
    #检查mariadb是否启动，等待5秒钟，再次检查mariadb启动
    DB_IS_RUN=`docker ps --filter "name=mariadb" --filter "status=running" | wc -l `
    if [ $DB_IS_RUN -ne 2 ]; then
        echo "mariadb is not running !!!"
    else
        #执行创建数据库
        docker exec -it mariadb mysql -uroot -pmariadb mysql -e \
            " CREATE DATABASE IF NOT EXISTS stock_data CHARACTER SET utf8 COLLATE utf8_general_ci "
        echo "CREATE stock_data DATABASE "
    fi
fi

#检查stock启动
STOCK_IS_RUN=`docker ps --filter "name=stock" --filter "status=running" | wc -l `
if [ $STOCK_IS_RUN -ge 2 ]; then
    echo "stop & rm stock ..."
    docker stop stock && docker rm stock
fi

sleep 1

echo "starting stock ..."
# 1 是开发环境。映射本地代码。
if [ $# == 1 ] ; then
    echo "#############  run dev ############# "
    # /data/stock 是代码目录 -v /data/stock:/data/stock 是开发模式。
    mkdir -p notebooks
    PWD=`pwd`
    docker run -itd --link=mariadb --name stock  \
      -p 8888:8888 -p 9999:9999 --restart=always \
      -v ${PWD}/jobs:/data/stock/jobs \
      -v ${PWD}/libs:/data/stock/libs \
      -v ${PWD}/web:/data/stock/web \
      -v ${PWD}/supervisor:/data/supervisor \
      -v ${PWD}/notebooks:/data/notebooks \
       pythonstock/pythonstock:latest
    exit 1;
else
    echo "############# run online ############# "
    # /data/stock 是代码目录 -v /data/stock:/data/stock 是开发模式。
    docker run -itd --link=mariadb --name stock  \
      -p 8888:8888 -p 9999:9999 --restart=always \
       pythonstock/pythonstock:latest
    exit 1;
fi

