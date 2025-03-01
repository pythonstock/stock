#!/bin/sh

export PYTHONIOENCODING=utf-8
export LANG=zh_CN.UTF-8
export PYTHONPATH=/data/stock
export LC_CTYPE=zh_CN.UTF-8

mkdir -p /data/logs/tensorflow



DATE=`date +%Y-%m-%d:%H:%M:%S`

echo $DATE >> /data/logs/run_cron.log

# 解决定时任务不启动问题，因为权限导致
chmod 755 /etc/cron.minutely/* && chmod 755 /etc/cron.hourly/*
chmod 755 /etc/cron.daily/* && chmod 755 /etc/cron.monthly/*

# 配置文件每次都设置权限
chmod 600 /var/spool/cron/crontabs/root
chown root:root /var/spool/cron/crontabs/root

#启动cron服务。在前台
/usr/sbin/cron -f