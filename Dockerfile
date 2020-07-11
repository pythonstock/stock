# 拆分基础镜像： docker/dockerfile


# 基础镜像，按照季度，月度更新。不影响应用镜像的构建。

FROM pythonstock/pythonstock:base-2020-07

WORKDIR /data

#add cron sesrvice.
#每分钟，每小时1分钟，每天1点1分，每月1号执行
RUN mkdir -p /etc/cron.minutely && mkdir -p /etc/cron.hourly && mkdir -p /etc/cron.monthly && \
    echo "SHELL=/bin/sh \n\
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin \n\
# min   hour    day     month   weekday command \n\
*/1     *       *       *       *       /bin/run-parts /etc/cron.minutely \n\
10       *       *       *       *       /bin/run-parts /etc/cron.hourly \n\
30       16       *       *       *       /bin/run-parts /etc/cron.daily \n\
30       17       1,10,20       *       *       /bin/run-parts /etc/cron.monthly \n" > /var/spool/cron/crontabs/root && \
    chmod 600 /var/spool/cron/crontabs/root


#增加服务端口就两个 6006 8500 9001
EXPOSE 8888 9999

#经常修改放到最后：
ADD jobs /data/stock/jobs
ADD libs /data/stock/libs
ADD web /data/stock/web
ADD supervisor /data/supervisor

ADD jobs/cron.minutely /etc/cron.minutely
ADD jobs/cron.hourly /etc/cron.hourly
ADD jobs/cron.daily /etc/cron.daily
ADD jobs/cron.monthly /etc/cron.monthly

RUN mkdir -p /data/logs && ls /data/stock/ && chmod 755 /data/stock/jobs/run_* &&  \
    chmod 755 /etc/cron.minutely/* && chmod 755 /etc/cron.hourly/* && \
    chmod 755 /etc/cron.daily/* && chmod 755 /etc/cron.monthly/*

ENTRYPOINT ["supervisord","-n","-c","/data/supervisor/supervisord.conf"]