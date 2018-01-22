# 降级使用python2. 为了兼容 TensorFlow-serving。
FROM docker.io/tensorflow/tensorflow:latest

# https://mirrors.aliyun.com/help/debian
# https://mirrors.aliyun.com/help/ubuntu
# https://mirrors.aliyun.com/help/centos

RUN echo  "deb http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse \n\
deb http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse \n\
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse \n\
deb http://mirrors.aliyun.com/ubuntu/ xenial-proposed main restricted universe multiverse \n\
deb http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse \n\
deb-src http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse \n\
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse \n\
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse \n\
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-proposed main restricted universe multiverse \n\
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse " > /etc/apt/sources.list

RUN echo  "[global]\n\
trusted-host=mirrors.aliyun.com\n\
index-url=http://mirrors.aliyun.com/pypi/simple" > /etc/pip.conf

#timezone
RUN apt-get update && apt-get install -y tzdata  && \
    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone && \
    apt-get clean

#install other lib
RUN apt-get update && apt-get install -y python-dev libmysqlclient-dev libhdf5-dev && \
    pip install mysqlclient  && \
    pip install sqlalchemy && \
    pip install requests && \
    apt-get install -y libxml2-dev && pip install lxml bs4 && \
    pip install tushare && \
    apt-get clean && apt-get remove -y python-dev libmysqlclient-dev && \
    pip install unittest2 && \
    pip install torndb && \
    pip install bcrypt && \
    pip install --upgrade tables

#1.解决 pandas 数据插入问题。直接修改数据库驱动 sqlalchemy 修改：statement.replace("INSERT INTO","INSERT IGNORE INTO")
# /usr/local/lib/python2.7/dist-packages/sqlalchemy/dialects/mysql/mysqldb.py
# 增加了一个 IGNORE 参数。
#2.解决torndb在python下面的问题：
#http://blog.csdn.net/littlethunder/article/details/8917378
RUN echo `date +%Y-%m-%d:%H:%M:%S` >> /etc/docker.build && \
    sed -i -e 's/executemany(statement/executemany(statement.replace\("INSERT INTO","INSERT IGNORE INTO")/g' \
        /usr/local/lib/python2.7/dist-packages/sqlalchemy/dialects/mysql/mysqldb.py && \
    rm -f /etc/cron.daily/apt-compat /etc/cron.daily/dpkg /etc/cron.daily/passwd && \
    sed -i -e 's/itertools\.izip/zip/g' \
    /usr/local/lib/python2.7/dist-packages/torndb.py


#增加语言utf-8
ENV LANG=en_US.UTF-8
ENV LC_CTYPE=en_US.UTF-8
ENV LC_ALL=C

WORKDIR /data

RUN pip install statsmodels bokeh stockstats alphalens pyfolio supervisor && \
    apt-get update && apt-get install -y quantlib-python net-tools


#add cron sesrvice.
#每分钟，每小时1分钟，每天1点1分，每月1号执行
RUN apt-get update && apt-get install -y cron vim && \
    mkdir -p /etc/cron.minutely && \
    echo "SHELL=/bin/sh \n\
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin \n\
# min   hour    day     month   weekday command \n\
*/1     *       *       *       *       /bin/run-parts /etc/cron.minutely \n\
10       *       *       *       *       /bin/run-parts /etc/cron.hourly \n\
30       16       *       *       *       /bin/run-parts /etc/cron.daily \n\
30       17       1,10,20       *       *       /bin/run-parts /etc/cron.monthly \n" > /var/spool/cron/crontabs/root && \
    chmod 600 /var/spool/cron/crontabs/root


#增加服务端口
EXPOSE 8888 9999 6006 8500 9001

#经常修改放到最后：
ADD jobs /data/stock/jobs
ADD libs /data/stock/libs
ADD tf /data/stock/tf
ADD web /data/stock/web
ADD supervisor /etc/supervisor

ADD jobs/cron.minutely /etc/cron.minutely
ADD jobs/cron.hourly /etc/cron.hourly
ADD jobs/cron.daily /etc/cron.daily
ADD jobs/cron.monthly /etc/cron.monthly

RUN mkdir -p /data/logs && ls /data/stock/ && chmod 755 /data/stock/jobs/run_* &&  \
    chmod 755 /etc/cron.minutely/* && chmod 755 /etc/cron.hourly/* && \
    chmod 755 /etc/cron.daily/* && chmod 755 /etc/cron.monthly/* && \
    ln -s /data/stock/libs/ /usr/lib/python2.7/libs && \
    ln -s /data/stock/web/ /usr/lib/python2.7/web

ENTRYPOINT ["supervisord","-n","-c","/etc/supervisor/supervisord.conf"]