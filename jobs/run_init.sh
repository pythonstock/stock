#!/bin/sh

mkdir -p /data/logs
DATE=`date +%Y-%m-%d:%H:%M:%S`

echo $DATE >> /data/logs/run_init.log

/usr/bin/python3.5 /data/stock/jobs/daily_job1.py  >> /data/logs/run_init.log