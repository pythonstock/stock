
# python 基础镜像

基础镜像升级到 2020年7月的版本

保证运行的最少基础环境，基础环境使用python3.6的版本。安装了超级多的lib库。非常的好用。

mysqlclient
sqlalchemy
requests
numpy
tushare
tornado torndb
bokeh
stockstats
ta-lib
jupyter
sklearn

# 2021年6月版本，使用 akshare 替换掉 tushare 库

akshare 地址：

https://www.akshare.xyz/zh_CN/latest/introduction.html

AKShare 是基于 Python 的财经数据接口库, 目的是实现对股票、期货、期权、基金、外汇、债券、指数、
加密货币等金融产品的基本面数据、实时和历史行情数据、衍生数据从数据采集、数据清洗到数据落地的一套工具, 
主要用于学术研究目的。


# 2021年 9 月版本，镜像裁剪，supervisor 使用python3

supervisor 使用 python3 后好像减少了不少大小。
同时删除掉一直没有用的 ta-lib 和 jupyter 。升级python基础镜像。

