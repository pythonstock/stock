#!/bin/sh


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
    docker run --name mariadb -v /data/mariadb/data:/var/lib/mysql \
    -e MYSQL_ROOT_PASSWORD=mariadb -p 3306:3306 -d mariadb:latest
    echo "starting mariadb ..."
else
    echo "mariadb is running !!!"
fi

####################### 创建数据库 #######################
echo "wait 5 second , and create stock database ."
sleep 5
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