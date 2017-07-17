### 1，股票系统设计

股票数据抓取框架使用TuShare。
http://tushare.org/

数据分析清洗使用pandas，numpy。
http://pandas.pydata.org/

数据存储到磁盘上，不使用数据库。存储PyTabe，hdf5格式。
http://www.pytables.org/

web框架使用tornado
http://www.tornadoweb.org/en/stable/

机器学习，当然使用最流行TensorFlow啦。
https://www.tensorflow.org/

数据展示使用 echarts
http://echarts.baidu.com/


### 2，架构设计
全系使用python实现。因为都是python的类库，互相之间调用方便。
从数据抓取，数据处理，到数据展示数据运算都是python实现。

最终的数据都到前端展示出来。主要分为4个文件夹。

> jobs 抓取数据并存储实现类。

> libs 通用工具类。

> web 前端展示框架。

> tf 机器学习文件夹，推测数据。
