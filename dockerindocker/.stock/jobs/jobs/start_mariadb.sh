#!/bin/sh

DATE=`date +%Y-%m-%d:%H:%M:%S`
echo $DATE

if [ ! -d "/data/mariadb" ]; then
    mkdir -p /data/mariadb
    /usr/bin/mysql_install_db
fi


/usr/bin/mysqld_safe >> /data/logs/start_mariadb.log