#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


import libs.common as common
import sys
import time
import pandas as pd
from sqlalchemy.types import NVARCHAR
from sqlalchemy import inspect
import datetime
import akshare as ak

"""
交易数据

# 历史行情数据
# 日频率
# 接口: stock_zh_a_daily
# 目标地址: https://finance.sina.com.cn/realstock/company/sh600006/nc.shtml(示例)
# 描述: A 股数据是从新浪财经获取的数据, 历史数据按日频率更新; 注意其中的 sh689009 为 CDR, 请 通过 stock_zh_a_cdr_daily 接口获取
# 限量: 单次返回指定 A 股上市公司指定日期间的历史行情日频率数据
# adjust=""; 默认为空: 返回不复权的数据; qfq: 返回前复权后的数据; hfq: 返回后复权后的数据;

"""

def stat_index_all(tmp_datetime):
    datetime_str = (tmp_datetime).strftime("%Y-%m-%d")
    datetime_int = (tmp_datetime).strftime("%Y%m%d")
    print("datetime_str:", datetime_str)
    print("datetime_int:", datetime_int)


    data = ak.stock_zh_a_spot()
    # 处理重复数据，保存最新一条数据。最后一步处理，否则concat有问题。
    if not data is None and len(data) > 0:
        # 插入数据库。
        # del data["reason"]
        data["date"] = datetime_int  # 修改时间成为int类型。
        data = data.drop_duplicates(subset="code", keep="last")
        data.head(n=1)
        common.insert_db(data, "stock_zh_a_spot", False, "`date`,`code`")
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

    # data = ts.get_index()
    # # 处理重复数据，保存最新一条数据。最后一步处理，否则concat有问题。
    # if not data is None and len(data) > 0:
    #     # 插入数据库。
    #     # del data["reason"]
    #     data["date"] = datetime_int  # 修改时间成为int类型。
    #     data = data.drop_duplicates(subset="code", keep="last")
    #     data.head(n=1)
    #     common.insert_db(data, "ts_index_all", False, "`date`,`code`")
    # else:
    #     print("no data .")

    print(datetime_str)


# main函数入口
if __name__ == '__main__':
    # 使用方法传递。
    tmp_datetime = common.run_with_args(stat_index_all)
    time.sleep(5)  # 停止5秒
    tmp_datetime = common.run_with_args(stat_today_all)
