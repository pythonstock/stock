#!/bin/bash

export PYTHONIOENCODING=utf-8
export LANG=zh_CN.UTF-8
export PYTHONPATH=/data/stock
export LC_CTYPE=zh_CN.UTF-8

echo "" > /data/logs/web.log
/usr/local/bin/python3 /data/stock/web/main.py -log_file_prefix=/data/logs/web.log