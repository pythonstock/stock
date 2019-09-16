### 使用方法（依赖docker）

已经放到docker hub上了

```
mkdir -p /data/mariadb/data
docker pull pythonstock/pythonstock:latest
docker pull mariadb:latest

docker run --name mariadb -v /data/mariadb/data:/var/lib/mysql \
    -e MYSQL_ROOT_PASSWORD=mariadb -p 3306:3306 -d mariadb:latest

docker run -itd --link=mariadb --name stock  \
    -v /data/notebooks:/data/notebooks \
    -p 8888:8888 \
    -p 9999:9999 \
    pythonstock/pythonstock:latest

```

### 更新日志

##1，增加 jupyter 和 TensorFlow 1.14.0



### 本地构建

其中构建文件参考 Dockerfile

首先会下载相关镜像，然后在进行构建。启动mariadb，并讲stock和mariadb链接起来。

```
依赖这两个镜像，tensorflow镜像比较大。
docker.io/python:3.6-slim
docker.io/mariadb:latest
```

### 访问端口

> http://localhost:9999 web 
>
> http://localhost:8888 jupyter

查看jupyter的密码：

```
docker exec -it stock bash 
cat /tmp/jupyter-stderr*.log
# 就可以看到 token 了，然后可以登录了。
```

### 1，股票系统设计

相关博客资料：
http://blog.csdn.net/freewebsys/article/category/7076584

股票数据抓取框架使用TuShare。
http://tushare.org/

数据分析清洗使用pandas，numpy。
http://pandas.pydata.org/

数据存储到磁盘上，使用Mysql数据库。存储股票数据。
https://pypi.python.org/pypi/mysqlclient

web框架使用tornado
http://www.tornadoweb.org/en/stable/

机器学习，当然使用最流行TensorFlow啦。
https://www.tensorflow.org/

tornado web系统
http://docs.pythontab.com/tornado/introduction-to-tornado/


### 2，架构设计
全系使用python实现。因为都是python的类库，互相之间调用方便。
从数据抓取，数据处理，到数据展示数据运算都是python实现。

最终的数据都到前端展示出来。主要分为4个文件夹。

> jobs 抓取数据并存储实现类。

> libs 通用工具类。

> web 前端展示框架。

> tf 机器学习文件夹，推测数据。

### 3，应用部署

需要mysql数据库启动。项目放到/data/stock 目录。
```
CREATE DATABASE IF NOT EXISTS `stock_data` CHARACTER SET utf8 COLLATE utf8_general_ci;
```

使用 :

http://docs.sqlalchemy.org/en/latest/core/reflection.html

### 3，web使用datatable显示报表

显示货币供应量：
 ![image](https://raw.githubusercontent.com/pythonstock/stock/master/web/static/img/stock-data-01.png)

 显示存款准备金率：
 ![image](https://raw.githubusercontent.com/pythonstock/stock/master/web/static/img/stock-data-02.png)

### 4，使用pandas处理重复数据

https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.drop_duplicates.html

```python
    data = ts.get_report_data(year, quarter)
    # 处理重复数据，保存最新一条数据。
    data.drop_duplicates(subset="code", keep="last")
```

### 5，增加多字段排序

> 1，点击是单个字段进行排序。
>
> 2，按照【shift】，点击多个，即可完成多字段排序。
> 
> 3，服务端分页排序。
>
> 4，按照多个字段进行筛选查询。

 ![image](https://raw.githubusercontent.com/pythonstock/stock/master/web/static/img/stock-data-04.png)


### 6，增加对字典表通用修改

```
CREATE TABLE `user_stock` (
  `code` varchar(255) NOT NULL,
  `date` varchar(8) NOT NULL,
  `price` double DEFAULT NULL,
  `shares` double DEFAULT NULL,
  `commission_rate` double DEFAULT NULL,
  `tax_rate` double DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

```

```
