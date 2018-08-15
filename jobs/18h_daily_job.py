#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


import libs.common as common
import sys
import time
import pandas as pd
import tushare as ts
from sqlalchemy.types import NVARCHAR
from sqlalchemy import inspect
import datetime

"""
交易数据

http://tushare.org/trading.html#id2

股市交易时间为每周一到周五上午时段9:30-11:30，下午时段13:00-15:00。 周六、周日上海证券交易所、深圳证券交易所公告的休市日不交易。

"""

def stat_index_all(tmp_datetime):
    datetime_str = (tmp_datetime).strftime("%Y-%m-%d")
    datetime_int = (tmp_datetime).strftime("%Y%m%d")
    print("datetime_str:", datetime_str)
    print("datetime_int:", datetime_int)


    data = ts.get_index()
    # 处理重复数据，保存最新一条数据。最后一步处理，否则concat有问题。
    if not data is None and len(data) > 0:
        # 插入数据库。
        # del data["reason"]
        data["date"] = datetime_int  # 修改时间成为int类型。
        data = data.drop_duplicates(subset="code", keep="last")
        data.head(n=1)
        common.insert_db(data, "ts_index_all", False, "`date`,`code`")
    else:
        print("no data .")

    print(datetime_str)

def stat_today_all(tmp_datetime):
    datetime_str = (tmp_datetime).strftime("%Y-%m-%d")
    datetime_int = (tmp_datetime).strftime("%Y%m%d")
    print("datetime_str:", datetime_str)
    print("datetime_int:", datetime_int)
    data = ts.get_today_all()
    # 处理重复数据，保存最新一条数据。最后一步处理，否则concat有问题。
    if not data is None and len(data) > 0:
        # 插入数据库。
        # del data["reason"]
        data["date"] = datetime_int  # 修改时间成为int类型。
        data = data.drop_duplicates(subset="code", keep="last")
        data.head(n=1)
        common.insert_db(data, "ts_today_all", False, "`date`,`code`")
    else:
        print("no data .")

    time.sleep(5)  # 停止5秒

    data = ts.get_index()
    # 处理重复数据，保存最新一条数据。最后一步处理，否则concat有问题。
    if not data is None and len(data) > 0:
        # 插入数据库。
        # del data["reason"]
        data["date"] = datetime_int  # 修改时间成为int类型。
        data = data.drop_duplicates(subset="code", keep="last")
        data.head(n=1)
        common.insert_db(data, "ts_index_all", False, "`date`,`code`")
    else:
        print("no data .")

    print(datetime_str)


# main函数入口
if __name__ == '__main__':
    # 使用方法传递。
    tmp_datetime = common.run_with_args(stat_index_all)
    time.sleep(5)  # 停止5秒
    tmp_datetime = common.run_with_args(stat_today_all)
