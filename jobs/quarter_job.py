#!/usr/local/bin/python
# -*- coding: utf-8 -*-


import libs.common as common
import sys
import time
import pandas as pd
import tushare as ts
from sqlalchemy.types import NVARCHAR
from sqlalchemy import inspect
import datetime


#############################基本面数据 http://tushare.org/fundamental.html
def stat_all(tmp_datetime):

    # 股票列表
    data = ts.get_stock_basics()
    print(data.index)
    common.insert_db(data, "ts_stock_basics", True, "`code`")




# main函数入口
if __name__ == '__main__':
    # 使用方法传递。
    tmp_datetime = common.run_with_args(stat_all)
