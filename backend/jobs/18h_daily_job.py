#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


import libs.common as common
import sys
import time
import pandas as pd
import numpy as np
from sqlalchemy.types import NVARCHAR
from sqlalchemy import inspect
import datetime
import akshare as ak
import traceback
import MySQLdb

# 600开头的股票是上证A股，属于大盘股
# 600开头的股票是上证A股，属于大盘股，其中6006开头的股票是最早上市的股票，
# 6016开头的股票为大盘蓝筹股；900开头的股票是上证B股；
# 000开头的股票是深证A股，001、002开头的股票也都属于深证A股，
# 其中002开头的股票是深证A股中小企业股票；
# 200开头的股票是深证B股；
# 300开头的股票是创业板股票；400开头的股票是三板市场股票。
def stock_a(code):
    # print(code)
    # print(type(code))
    # 上证A股  # 深证A股
    if code.startswith('600') or code.startswith('6006') or code.startswith('601') or code.startswith('000') or code.startswith('001') or code.startswith('002'):
        return True
    else:
        return False
# 过滤掉 st 股票。
def stock_a_filter_st(name):
    # print(code)
    # print(type(code))
    # 上证A股  # 深证A股
    if name.find("ST") == -1:
        return True
    else:
        return False

# 过滤价格，如果没有基本上是退市了。
def stock_a_filter_price(latest_price):
    # float 在 pandas 里面判断 空。
    if np.isnan(latest_price):
        return False
    else:
        return True

####### 3.pdf 方法。宏观经济数据
# 接口全部有错误。只专注股票数据。
def stat_all(tmp_datetime):

    datetime_str = (tmp_datetime).strftime("%Y-%m-%d")
    datetime_int = (tmp_datetime).strftime("%Y%m%d")
    print("datetime_str:", datetime_str)
    print("datetime_int:", datetime_int)

    # 股票列表
    try:
        data = ak.stock_zh_a_spot_em()
        # print(data.index)
        # 解决ESP 小数问题。
        # data["esp"] = data["esp"].round(2)  # 数据保留2位小数
        data.columns = ['index', 'code', 'name', 'last_price', 'change_percent', 'change_amount',
        'volume', 'turnover', 'amplitude', 'high', 'low', 'open', 'closed', 'volume_ratio',
        'turnover_rate', 'pe_ratio','pb_ratio', 'market_cap','circulating_market_cap','rise_speed',
        'change_5min', 'change_ercent_60day','ytd_change_percent']

        data = data.loc[data["code"].apply(stock_a)].loc[data["name"].apply(stock_a_filter_st)].loc[
            data["last_price"].apply(stock_a_filter_price)]
        print(data)
        data['date'] = datetime_int  # 修改时间成为int类型。

        # 删除老数据。
        del_sql = " DELETE FROM `stock_zh_a_spot_em` where `date` = '%s' " % datetime_int
        common.insert(del_sql)

        data.set_index('code', inplace=True)
        data.drop('index', axis=1, inplace=True)
        print(data)
        # 删除index，然后和原始数据合并。
        common.insert_db(data, "stock_zh_a_spot_em", True, "`date`,`code`")
    except Exception as e:
        print("error :", e)
        traceback.print_exc()



    # 龙虎榜-个股上榜统计
    # 接口: stock_lhb_ggtj_sina
    #
    # 目标地址: http://vip.stock.finance.sina.com.cn/q/go.php/vLHBData/kind/ggtj/index.phtml
    #
    # 描述: 获取新浪财经-龙虎榜-个股上榜统计
    #

    try:
        stock_lhb_ggtj_sina = ak.stock_lhb_ggtj_sina(symbol="5")
        print(stock_lhb_ggtj_sina)

        stock_lhb_ggtj_sina.columns = ['code', 'name', 'ranking_times', 'sum_buy', 'sum_sell', 'net_amount', 'buy_seat',
                                       'sell_seat']

        stock_lhb_ggtj_sina = stock_lhb_ggtj_sina.loc[stock_lhb_ggtj_sina["code"].apply(stock_a)].loc[
            stock_lhb_ggtj_sina["name"].apply(stock_a_filter_st)]

        stock_lhb_ggtj_sina.set_index('code', inplace=True)
        # data_sina_lhb.drop('index', axis=1, inplace=True)
        # 删除老数据。
        stock_lhb_ggtj_sina['date'] = datetime_int  # 修改时间成为int类型。

        # 删除老数据。
        del_sql = " DELETE FROM `stock_lhb_ggtj_sina` where `date` = '%s' " % datetime_int
        common.insert(del_sql)

        common.insert_db(stock_lhb_ggtj_sina, "stock_lhb_ggtj_sina", True, "`date`,`code`")

    except Exception as e:
        print("error :", e)
        traceback.print_exc()
        


    # 每日统计
    # 接口: stock_dzjy_mrtj
    #
    # 目标地址: http://data.eastmoney.com/dzjy/dzjy_mrtj.aspx
    #
    # 描述: 获取东方财富网-数据中心-大宗交易-每日统计
    # https://akshare.akfamily.xyz/data/stock/stock.html#id318
    # import akshare as ak
    # stock_dzjy_mrtj_df = ak.stock_dzjy_mrtj(start_date='20220105', end_date='20220105')
    # print(stock_dzjy_mrtj_df)

    try:

        print("################ tmp_datetime : " + datetime_int)
        # 格式要 int类型日期
        stock_dzjy_mrtj = ak.stock_dzjy_mrtj(start_date=datetime_int, end_date=datetime_int)
        print(stock_dzjy_mrtj)

        stock_dzjy_mrtj.columns = ['index', 'trade_date', 'code', 'name', 'quote_change', 'close_price', 'average_price',
                                   'overflow_rate', 'trade_number', 'sum_volume', 'sum_turnover',
                                   'turnover_market_rate']

        stock_dzjy_mrtj.set_index('code', inplace=True)
        # data_sina_lhb.drop('index', axis=1, inplace=True)
        # 删除老数据。
        stock_dzjy_mrtj['date'] = datetime_int  # 修改时间成为int类型。
        stock_dzjy_mrtj.drop('trade_date', axis=1, inplace=True)
        stock_dzjy_mrtj.drop('index', axis=1, inplace=True)

        # 数据保留2位小数
        try:
            stock_dzjy_mrtj = stock_dzjy_mrtj.loc[stock_dzjy_mrtj["code"].apply(stock_a)].loc[
                stock_dzjy_mrtj["name"].apply(stock_a_filter_st)]

            stock_dzjy_mrtj["average_price"] = stock_dzjy_mrtj["average_price"].round(2)
            stock_dzjy_mrtj["overflow_rate"] = stock_dzjy_mrtj["overflow_rate"].round(4)
            stock_dzjy_mrtj["turnover_market_rate"] = stock_dzjy_mrtj["turnover_market_rate"].round(6)
        except Exception as e:
            print("round error :", e)
            traceback.print_exc()

        # 删除老数据。
        del_sql = " DELETE FROM `stock_dzjy_mrtj` where `date` = '%s' " % datetime_int
        common.insert(del_sql)

        print(stock_dzjy_mrtj)

        common.insert_db(stock_dzjy_mrtj, "stock_dzjy_mrtj", True, "`date`,`code`")

    except Exception as e:
        print("error :", e)
        traceback.print_exc()

# main函数入口
if __name__ == '__main__':
    # 执行数据初始化。
    # 使用方法传递。
    tmp_datetime = common.run_with_args(stat_all)
