#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


import libs.common as common
import sys
import os
import time
import pandas as pd
import tushare as ts
from sqlalchemy.types import NVARCHAR
from sqlalchemy import inspect
import datetime
import shutil


####### 使用 5.pdf，先做 基本面数据 的数据，然后在做交易数据。
#
def stat_all(tmp_datetime):
    datetime_str = (tmp_datetime).strftime("%Y-%m-%d")
    datetime_int = (tmp_datetime).strftime("%Y%m%d")

    cache_dir = common.bash_stock_tmp % (datetime_str[0:7], datetime_str)
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
        print("remove cache dir force :", cache_dir)

    print("datetime_str:", datetime_str)
    print("datetime_int:", datetime_int)
    data = ts.top_list(datetime_str)
    # 处理重复数据，保存最新一条数据。最后一步处理，否则concat有问题。
    #
    if not data is None and len(data) > 0:
        # 插入数据库。
        # del data["reason"]
        data["date"] = datetime_int  # 修改时间成为int类型。
        data = data.drop_duplicates(subset="code", keep="last")
        data.head(n=1)
        common.insert_db(data, "ts_top_list", False, "`date`,`code`")
    else:
        print("no data .")

    print(datetime_str)


# main函数入口
if __name__ == '__main__':
    # 使用方法传递。
    tmp_datetime = common.run_with_args(stat_all)
