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


# 增加一个新quarter列，用来存储季度信息。
def concat_quarter(year, quarter, data_array):
    print(len(data_array))
    quarter_str = str(year) + str("%02d" % quarter)  # 格式化季度数据。2位。
    # 增加到列。
    quarter_col = pd.DataFrame([quarter_str for _ in range(len(data_array))], columns=["quarter"])
    return pd.concat([quarter_col, data_array], axis=1)


#############################基本面数据 http://tushare.org/fundamental.html
def stat_all(tmp_datetime):
    # 返回 31 天前的数据，做上个季度数据统计。
    tmp_datetime_1month = tmp_datetime + datetime.timedelta(days=-31)
    year = int((tmp_datetime_1month).strftime("%Y"))
    quarter = int(pd.Timestamp(tmp_datetime_1month).quarter)  # 获得上个季度的数据。
    print("############ year %d, quarter %d", year, quarter)
    # 业绩报告（主表）
    data = ts.get_report_data(year, quarter)
    # 增加季度字段。
    data = concat_quarter(year, quarter, data)
    # 处理重复数据，保存最新一条数据。最后一步处理，否则concat有问题。
    data = data.drop_duplicates(subset="code", keep="last")
    # 插入数据库。
    common.insert_db(data, "ts_report_data", False, "`quarter`,`code`")

    # 盈利能力
    data = ts.get_profit_data(year, quarter)
    # 增加季度字段。
    data = concat_quarter(year, quarter, data)
    # 处理重复数据，保存最新一条数据。
    data = data.drop_duplicates(subset="code", keep="last")
    # 插入数据库。
    common.insert_db(data, "ts_profit_data", False, "`quarter`,`code`")

    # 营运能力
    data = ts.get_operation_data(year, quarter)
    # 增加季度字段。
    data = concat_quarter(year, quarter, data)
    # 处理重复数据，保存最新一条数据。最后一步处理，否则concat有问题。
    data = data.drop_duplicates(subset="code", keep="last")
    # 插入数据库。
    common.insert_db(data, "ts_operation_data", False, "`quarter`,`code`")

    # 成长能力
    data = ts.get_growth_data(year, quarter)
    # 增加季度字段。
    data = concat_quarter(year, quarter, data)
    # 处理重复数据，保存最新一条数据。最后一步处理，否则concat有问题。
    data = data.drop_duplicates(subset="code", keep="last")
    # 插入数据库。
    common.insert_db(data, "ts_growth_data", False, "`quarter`,`code`")

    # 偿债能力
    data = ts.get_debtpaying_data(year, quarter)
    # 增加季度字段。
    data = concat_quarter(year, quarter, data)
    # 处理重复数据，保存最新一条数据。最后一步处理，否则concat有问题。
    data = data.drop_duplicates(subset="code", keep="last")
    # 插入数据库。
    common.insert_db(data, "ts_debtpaying_data", False, "`quarter`,`code`")

    # 现金流量
    data = ts.get_cashflow_data(year, quarter)
    # 增加季度字段。
    data = concat_quarter(year, quarter, data)
    # 处理重复数据，保存最新一条数据。最后一步处理，否则concat有问题。
    data = data.drop_duplicates(subset="code", keep="last")
    # 插入数据库。
    common.insert_db(data, "ts_cashflow_data", False, "`quarter`,`code`")


# main函数入口
if __name__ == '__main__':
    # 使用方法传递。
    tmp_datetime = common.run_with_args(stat_all)
