#使用 python:3.8-slim 做基础镜像减少大小。其中tensorflow再用另外的镜像跑数据。

# 之前使用的是python:3.6-slim
# 可以更新 3.8-slim-bullseye slim-bullseye

# https://hub.docker.com/_/python?tab=tags&page=1&name=3.8-slim-bullseye
# 用这个做为基础镜像，防止每次都进行构建。

#FROM docker.io/python:3.8-slim-bullseye
#FROM hub.atomgit.com/amd64/python:3.8-slim-bullseye
# https://hub.atomgit.com/repos/amd64/python
#FROM hub.atomgit.com/amd64/python:3.11-slim-bullseye
FROM docker.m.daocloud.io/library/python:3.11-slim-bullseye

# https://opsx.alibaba.com/mirror
# 使用阿里云镜像地址。修改debian apt 更新地址，pip 地址，设置时区。
# 设置debian的镜像源
RUN echo "deb http://mirrors.aliyun.com/debian/ bullseye main non-free contrib" > /etc/apt/sources.list && \
echo "deb-src http://mirrors.aliyun.com/debian/ bullseye main non-free contrib" >> /etc/apt/sources.list && \
echo "deb http://mirrors.aliyun.com/debian-security/ bullseye-security main" >> /etc/apt/sources.list && \
echo "deb-src http://mirrors.aliyun.com/debian-security/ bullseye-security main" >> /etc/apt/sources.list && \
echo "deb http://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib" >> /etc/apt/sources.list && \
echo "deb-src http://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib" >> /etc/apt/sources.list && \
echo "deb http://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib" >> /etc/apt/sources.list && \
echo "deb-src http://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib" >> /etc/apt/sources.list && \
echo  "[global]\n\
trusted-host=mirrors.aliyun.com\n\
index-url=http://mirrors.aliyun.com/pypi/simple" > /etc/pip.conf && \
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone

#增加语言utf-8
ENV LANG=zh_CN.UTF-8
ENV LC_CTYPE=zh_CN.UTF-8
ENV LC_ALL=C
ENV PYTHONPATH=/data/stock

# 增加 TensorFlow 的支持，使用最新的2.0 编写代码。目前还是使用 1.x 吧，还没有学明白。
# RUN pip3 install tensorflow==2.0.0-rc1 keras
# RUN pip3 install tensorflow keras sklearn

# 设置 vim 的语言配置
RUN mkdir -p /etc/vim/ && \
    echo "set fileencodings=utf-8,ucs-bom,gb18030,gbk,gb2312,cp936" >> /etc/vim/vimrc && \
    echo "set termencoding=utf-8" >> /etc/vim/vimrc && \
    echo "set encoding=utf-8" >> /etc/vim/vimrc

# 安装 mysqlclient akshare (pandas ,numpy) tornado bokeh
# 安装 nodejs 库
# apt-get autoremove -y 删除没有用的依赖lib。减少镜像大小。1MB 也要节省。
# apt-get --purge remove 软件包名称 , 删除已安装包（不保留配置文件)。
RUN apt-get update && apt-get install -y git pkg-config net-tools procps gcc make python3-dev default-libmysqlclient-dev libxml2-dev cron  && \
    pip3 install mysqlclient sqlalchemy && \
    pip3 install supervisor && \
    pip3 install numpy pandas  && \
    pip3 install akshare --upgrade && \
    apt-get install -y nodejs && \
    pip3 install tornado torndb && \
    pip3 install bokeh stockstats scikit-learn && \
    apt-get --purge remove -y gcc make python3-dev default-libmysqlclient-dev libxml2-dev && \
    rm -rf /root/.cache/* && apt-get clean && apt-get autoremove -y  && \
    cd /usr/local/lib/python3.11/site-packages && find ./ -name *.pyc | xargs rm -f  

# /usr/local/lib/python3.11/site-packages/pandas/
# 1.解决 pandas 数据插入问题。直接修改数据库驱动 sqlalchemy
# 修改：statement.replace("INSERT INTO","INSERT IGNORE INTO")
# /usr/local/lib/python3.11/site-packages/sqlalchemy/dialects/mysql/mysqldb.py
# 增加了一个 IGNORE 参数。
# 2.解决torndb在python3下面的问题：
# http://blog.csdn.net/littlethunder/article/details/8917378
# 3. 解决 type 问题，使用sed 进行替换。
#  File "/usr/local/lib/python3.11/site-packages/torndb.py", line 260, in <module>
#    CONVERSIONS[field_type] = [(FLAG.BINARY, str)] + CONVERSIONS[field_type]
#  TypeError: can only concatenate list (not "type") to list

RUN echo `date +%Y-%m-%d:%H:%M:%S` >> /etc/docker.build && \
    sed -i -e 's/executemany(statement/executemany(statement.replace\("INSERT INTO","INSERT IGNORE INTO")/g' \
        /usr/local/lib/python3.11/site-packages/sqlalchemy/dialects/mysql/mysqldb.py && \
    rm -f /etc/cron.daily/apt-compat /etc/cron.daily/dpkg /etc/cron.daily/passwd && \
    sed -i -e 's/itertools\.izip/zip/g' \
    /usr/local/lib/python3.11/site-packages/torndb.py  && \
    sed -i -e 's/\+ CONVERSIONS\[field_type\]/\+ \[CONVERSIONS\[field_type\],bytes\]/g' \
    /usr/local/lib/python3.11/site-packages/torndb.py


#add cron sesrvice.
#每分钟，每小时1分钟，每天1点1分，每月1号执行
RUN mkdir -p /etc/cron.minutely && mkdir -p /etc/cron.hourly && mkdir -p /etc/cron.monthly && mkdir -p /var/spool/cron/crontabs && \
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

ENTRYPOINT ["supervisord","-n","-c","/data/supervisor/supervisord.conf"]

