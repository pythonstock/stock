#!/bin/sh

ps -ef | grep python3 | grep '/data/stock/web/main.py' | awk '{print$2}' | xargs kill -9
echo "restart web ... " > /data/logs/tornado.log
