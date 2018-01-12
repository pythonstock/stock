#!/bin/sh

mkdir -p /data/logs/tensorflow
mkdir -p /data/notebooks

DATE=`date +%Y-%m-%d:%H:%M:%S`

echo $DATE >> /data/logs/run_init.log

/usr/bin/python /data/stock/jobs/basic_job.py  >> /data/logs/run_init.log

#启动cron服务。在前台
/usr/sbin/cron -f