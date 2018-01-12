#!/bin/sh

ps -ef | grep python3 | grep '/data/stock/web/main.py' | awk '{print$2}' | xargs kill -9
echo "" > /data/logs/tornado.log
nohup /usr/bin/python /data/stock/web/main.py >> /data/logs/tornado.log &