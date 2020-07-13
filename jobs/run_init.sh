#!/bin/sh

export PYTHONIOENCODING=utf-8
export LANG=zh_CN.UTF-8
export PYTHONPATH=/data/stock
export LC_CTYPE=zh_CN.UTF-8

mkdir -p /data/logs/tensorflow

DATE=`date +%Y-%m-%d:%H:%M:%S`

echo $DATE >> /data/logs/run_init.log

/usr/local/bin/python3 /data/stock/jobs/basic_job.py  >> /data/logs/run_init.log

# https://stackoverflow.com/questions/27771781/how-can-i-access-docker-set-environment-variables-from-a-cron-job
# 解决环境变量输出问题。
printenv | grep -v "no_proxy" >> /etc/environment

# 第一次后台执行日数据。
nohup bash /data/stock/jobs/cron.daily/run_daily &

#启动cron服务。在前台
/usr/sbin/cron -f