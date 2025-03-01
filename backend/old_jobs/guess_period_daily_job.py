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
import heapq

"""
SELECT `date`, `code`, `name`, `changepercent`, `trade`, `open`, `high`, `low`, 
                `settlement`, `volume`, `turnoverratio`, `amount`, `per`, `pb`, `mktcap`, `nmc` 
    FROM stock_data.ts_today_all where `date` = 20171106 and trade > 0 and trade <= 20
and `code` not like '002%' and `code` not like '300%'  and `name` not like '%st%'

"""


def stat_index_all(tmp_datetime):
    datetime_str = (tmp_datetime).strftime("%Y-%m-%d")
    datetime_int = (tmp_datetime).strftime("%Y%m%d")
    print("datetime_str:", datetime_str)
    print("datetime_int:", datetime_int)

    # 查询今日满足股票数据。剔除数据：创业板股票数据，中小板股票数据，所有st股票
    # #`code` not like '002%' and `code` not like '300%'  and `name` not like '%st%'
    sql_1 = """ 
            SELECT `date`, `code`, `name`, `changepercent`, `trade`, `open`, `high`, `low`, 
                `settlement`, `volume`, `turnoverratio`, `amount`, `per`, `pb`, `mktcap`, `nmc` 
            FROM stock_data.ts_today_all WHERE `date` = %s and `trade` > 0 and `open` > 0 and trade <= 20 
                and `code` not like %s and `code` not like %s and `name` not like %s
            """
    print(sql_1)
    data = pd.read_sql(sql=sql_1, con=common.engine(), params=[datetime_int, '002%', '300%', '%st%'])
    print(type(data))
    data = data.drop_duplicates(subset="code", keep="last")
    print(data["trade"])
    data["trade_float32"] = data["trade"].astype('float32', copy=False)
    print(len(data))
    print("########data[trade]########:")
    print(data["trade"])

    # 使用 trade 填充数据
    stock_guess = pd.DataFrame({
        "date": data["date"], "code": data["code"], "wave_mean": data["trade"],
        "wave_crest": data["trade"], "wave_base": data["trade"]}, index=data.index.values)
    print(stock_guess.head())
    stock_guess = stock_guess.apply(apply_guess, axis=1)  # , axis=1)
    print(stock_guess.head())
    # stock_guess.astype('float32', copy=False)
    stock_guess.drop('date', axis=1, inplace=True)  # 删除日期字段，然后和原始数据合并。
    stock_guess = stock_guess.round(2)  # 数据保留2位小数
    print(stock_guess["wave_base"])

    data_new = pd.merge(data, stock_guess, on=['code'], how='left')
    print("#############")

    # 使用pandas 函数 ： https://pandas.pydata.org/pandas-docs/stable/api.html#id4
    data_new["up_rate"] = (data_new["trade_float32"].sub(data_new["wave_mean"])).div(data_new["wave_crest"]).mul(100)
    data_new["up_rate"] = data_new["up_rate"].round(2)  # 数据保留2位小数
    data_new.drop('trade_float32', axis=1, inplace=True)  # 删除计算字段。

    # 删除老数据。
    del_sql = " DELETE FROM `stock_data`.`guess_period_daily` WHERE `date`= '%s' " % datetime_int
    common.insert(del_sql)
    # print(data_new.head())
    # data_new["down_rate"] = (data_new["trade"] - data_new["wave_mean"]) / data_new["wave_base"]
    common.insert_db(data_new, "guess_period_daily", False, "`date`,`code`")

    # 进行左连接.
    # tmp = pd.merge(tmp, tmp2, on=['company_id'], how='left')


def apply_guess(tmp):
    date = tmp["date"]
    code = tmp["code"]
    date_end = datetime.datetime.strptime(date, "%Y%m%d")
    date_start = (date_end + datetime.timedelta(days=-300)).strftime("%Y-%m-%d")
    date_end = date_end.strftime("%Y-%m-%d")
    print(code, date_start, date_end)

    # open, high, close, low, volume, price_change, p_change, ma5, ma10, ma20, v_ma5, v_ma10, v_ma20, turnover
    # 使用缓存方法。加快计算速度。
    stock = common.get_hist_data_cache(code, date_start, date_end)
    # 增加空判断，如果是空返回 0 数据。
    if stock is None:
        return pd.Series([date, code, 0.0, 0.0, 0.0],
                     index=['date', 'code', 'wave_mean', 'wave_crest', 'wave_base'])

    stock = pd.DataFrame({"close": stock["close"]}, index=stock.index.values)
    stock = stock.sort_index(0)  # 将数据按照日期排序下。

    # print(stock.head(10))
    arr = pd.Series(stock["close"].values)
    # print(df_arr)
    wave_mean = arr.mean()
    # 计算股票的波峰值。
    wave_crest = heapq.nlargest(5, enumerate(arr), key=lambda x: x[1])
    wave_crest_mean = pd.DataFrame(wave_crest).mean()

    # 输出元祖第一个元素是index，第二元素是比较的数值 计算数据的波谷值
    wave_base = heapq.nsmallest(5, enumerate(arr), key=lambda x: x[1])
    wave_base_mean = pd.DataFrame(wave_base).mean()
    # 输出数据
    # print("##############")
    #     code      date wave_base wave_crest wave_mean 顺序必须一致。返回的是行数据，然后填充。
    return pd.Series([date, code, wave_base_mean[1], wave_crest_mean[1], wave_mean],
                     index=['date','code','wave_mean','wave_crest','wave_base'])


# main函数入口
if __name__ == '__main__':
    # 使用方法传递。
    tmp_datetime = common.run_with_args(stat_index_all)
