#!/bin/sh

mkdir -p /data/logs/tensorflow

DATE=`date +%Y-%m-%d:%H:%M:%S`

echo $DATE >> /data/logs/run_init.log

/usr/local/bin/python3 /data/stock/jobs/basic_job.py  >> /data/logs/run_init.log

# https://stackoverflow.com/questions/27771781/how-can-i-access-docker-set-environment-variables-from-a-cron-job
# 解决环境变量输出问题。
printenv | grep -v "no_proxy" >> /etc/environment

#启动cron服务。在前台
/usr/sbin/cron -f