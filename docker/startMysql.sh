#!/bin/sh


#判断文件夹存在不。
if [ ! -d "/data/mariadb/data" ]; then
    mkdir -p /data/mariadb/data
fi

HAS_DB=`docker images mariadb | wc -l `
if [ $HAS_DB -ne 2 ];then
    docker pull mariadb
fi

docker run --name mariadb -v /data/mariadb/data:/var/lib/mysql \
    -e MYSQL_ROOT_PASSWORD=mariadb -p 3306:3306 -d mariadb:latest

sleep 1
#检查mariadb是否启动，等待1秒钟
DB_IS_RUN=`docker ps --filter "name=mariadb" --filter "status=running" | wc -l `

if [ $DB_IS_RUN -ne 2 ]; then
    echo "mariadb is not running !!!"
else
    #执行创建数据库
    docker exec -it mariadb mysql -uroot -pmariadb mysql -e \
        " CREATE DATABASE IF NOT EXISTS stock_data CHARACTER SET utf8 COLLATE utf8_general_ci "
    echo "CREATE stock_data DATABASE "
fi



