#使用 python:3.7-slim 做基础镜像减少大小。其中tensorflow再用另外的镜像跑数据。

# 之前使用的是python:3.6-slim
# 可以更新 3.7-slim-stretch slim-stretch

# https://hub.docker.com/_/python?tab=tags&page=1&name=3.7-slim-stretch
# 用这个做为基础镜像，防止每次都进行构建。

FROM docker.io/python:3.7-slim-stretch

# https://opsx.alibaba.com/mirror
# 使用阿里云镜像地址。修改debian apt 更新地址，pip 地址，设置时区。
RUN echo  "deb http://mirrors.aliyun.com/debian/ stretch main non-free contrib\n\
deb-src http://mirrors.aliyun.com/debian/ stretch main non-free contrib\n\
deb http://mirrors.aliyun.com/debian-security stretch/updates main\n\
deb-src http://mirrors.aliyun.com/debian-security stretch/updates main\n\
deb http://mirrors.aliyun.com/debian/ stretch-updates main non-free contrib\n\
deb-src http://mirrors.aliyun.com/debian/ stretch-updates main non-free contrib\n\
deb http://mirrors.aliyun.com/debian/ stretch-backports main non-free contrib\n\
deb-src http://mirrors.aliyun.com/debian/ stretch-backports main non-free contrib" > /etc/apt/sources.list && \
echo  "[global]\n\
trusted-host=mirrors.aliyun.com\n\
index-url=http://mirrors.aliyun.com/pypi/simple" > /etc/pip.conf && \
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone

RUN echo "rebuild docker @2022-01-12"
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
RUN apt-get update && apt-get install -y net-tools procps gcc make python3-dev default-libmysqlclient-dev libxml2-dev cron  && \
    pip3 install mysqlclient sqlalchemy && \
    pip3 install supervisor && \
    pip3 install numpy pandas  && \
    pip3 install akshare --upgrade && \
    apt-get install -y nodejs && \
    pip3 install tornado torndb && \
    pip3 install bokeh stockstats sklearn && \
    apt-get --purge remove -y gcc make python3-dev default-libmysqlclient-dev libxml2-dev && \
    rm -rf /root/.cache/* && apt-get clean && apt-get autoremove -y

# /usr/local/lib/python3.7/site-packages/pandas/
# 1.解决 pandas 数据插入问题。直接修改数据库驱动 sqlalchemy
# 修改：statement.replace("INSERT INTO","INSERT IGNORE INTO")
# /usr/local/lib/python3.7/site-packages/sqlalchemy/dialects/mysql/mysqldb.py
# 增加了一个 IGNORE 参数。
# 2.解决torndb在python3下面的问题：
# http://blog.csdn.net/littlethunder/article/details/8917378
# 3. 解决 type 问题，使用sed 进行替换。
#  File "/usr/local/lib/python3.7/site-packages/torndb.py", line 260, in <module>
#    CONVERSIONS[field_type] = [(FLAG.BINARY, str)] + CONVERSIONS[field_type]
#  TypeError: can only concatenate list (not "type") to list

RUN echo `date +%Y-%m-%d:%H:%M:%S` >> /etc/docker.build && \
    sed -i -e 's/executemany(statement/executemany(statement.replace\("INSERT INTO","INSERT IGNORE INTO")/g' \
        /usr/local/lib/python3.7/site-packages/sqlalchemy/dialects/mysql/mysqldb.py && \
    rm -f /etc/cron.daily/apt-compat /etc/cron.daily/dpkg /etc/cron.daily/passwd && \
    sed -i -e 's/itertools\.izip/zip/g' \
    /usr/local/lib/python3.7/site-packages/torndb.py  && \
    sed -i -e 's/\+ CONVERSIONS\[field_type\]/\+ \[CONVERSIONS\[field_type\],bytes\]/g' \
    /usr/local/lib/python3.7/site-packages/torndb.py


