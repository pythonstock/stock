#!/bin/sh

mkdir -p /data/logs/tensorflow
DATE=`date +%Y-%m-%d:%H:%M:%S`

echo $DATE >> /data/logs/run_init.log

/usr/bin/python3 /data/stock/jobs/basic_job.py  >> /data/logs/run_init.log