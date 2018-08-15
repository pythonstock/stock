#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


import libs.common as common
import pandas as pd
import numpy as np
import math
import datetime
import heapq
import stockstats


# code      date today_trade
def apply_merge(tmp):
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
        return list([code, date, 0.0])
    print("########")
    # print(stock.tail(1))
    close = stock.tail(1)["close"].values[0]
    print("close:  ", close)
    print("########")
    return list([code, date, close])


#    buy    code      date  sell  sell_cci  sell_kdjj  sell_rsi_6
def apply_merge_sell(tmp):
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
        return list([1, code, date, 0, 0, 0, 0])
    print("########")
    # J大于100时为超买，小于10时为超卖。
    # 强弱指标保持高于50表示为强势市场，反之低于50表示为弱势市场。
    # 1、当CCI指标从下向上突破﹢100线而进入非常态区间时，表明股价脱离常态而进入异常波动阶段，
    # 2、当CCI指标从上向下突破﹣100线而进入另一个非常态区间时，表明股价的盘整阶段已经结束，
    stockStat = stockstats.StockDataFrame.retype(stock)
    kdjj = int(stockStat["kdjj"].tail(1).values[0])
    rsi_6 = int(stockStat["rsi_6"].tail(1).values[0])
    cci = int(stockStat["cci"].tail(1).values[0])
    print("kdjj:", kdjj, "rsi_6:", rsi_6, "cci:", cci)
    # and kdjj > 80 and rsi_6 > 55  and cci > 100 判断卖出时刻。也就是买入时刻的反面。发现有波动就卖了。
    # if kdjj <= 10 and rsi_6 <= 50 and cci <= 100: old
    if kdjj <= 80 or rsi_6 <= 55 or cci <= 100:
        return list([0, code, date, 1, cci, kdjj, rsi_6])
    else:
        return list([1, code, date, 0, cci, kdjj, rsi_6])


# 增加 收益计算。
def stat_index_calculate(tmp_datetime):
    # 要操作的数据库表名称。
    table_name = "guess_indicators_lite_sell_daily"
    datetime_str = (tmp_datetime).strftime("%Y-%m-%d")
    datetime_int = (tmp_datetime).strftime("%Y%m%d")
    print("datetime_str:", datetime_str)
    print("datetime_int:", datetime_int)

    sql_1 = """ 
                SELECT `buy_date`, `code`, `name`, `changepercent`, `trade`, `turnoverratio`, `pb`, `kdjj`, `rsi_6`, 
                `cci`, `wave_base`, `wave_crest`, `wave_mean`, `up_rate`
                FROM guess_indicators_lite_buy_daily where `buy_date` <= """ + datetime_int
    print(sql_1)
    data = pd.read_sql(sql=sql_1, con=common.engine(), params=[])
    data = data.drop_duplicates(subset="code", keep="last")
    print(data["trade"])
    data["trade_float32"] = data["trade"].astype('float32', copy=False)
    print(len(data))
    data["date"] = datetime_int

    stock_merge = pd.DataFrame({
        "date": data["date"], "code": data["code"], "today_trade": data["trade"]}, index=data.index.values)
    print(stock_merge.head(1))

    stock_merge = stock_merge.apply(apply_merge, axis=1)  # , axis=1)

    del stock_merge["date"]  # 合并前删除 date 字段。
    # 合并数据
    data_new = pd.merge(data, stock_merge, on=['code'], how='left')
    data_new["income"] = (data_new["today_trade"] - data_new["trade_float32"]) * 100
    data_new["income"] = data_new["income"].round(4)  # 保留4位小数。

    # 增加售出列。看看是否需要卖出。
    stock_sell_merge = pd.DataFrame({
        "date": data["date"], "code": data["code"], "sell": 0, "buy": 0, "sell_kdjj": 0, "sell_rsi_6": 0,
        "sell_cci": 0},
        index=data.index.values)
    print(stock_sell_merge.head(1))

    merge_sell_data = stock_sell_merge.apply(apply_merge_sell, axis=1)  # , axis=1)
    # 重命名
    del merge_sell_data["date"]  # 合并前删除 date 字段。
    # 合并数据
    data_new = pd.merge(data_new, merge_sell_data, on=['code'], how='left')

    # 删除老数据。
    try:
        del_sql = " DELETE FROM `stock_data`.`" + table_name + "` WHERE `date`= '%s' " % datetime_int
        common.insert(del_sql)
        print("insert_db")
    except Exception as e:
        print("error :", e)
    del data_new["trade_float32"]
    try:
        common.insert_db(data_new, table_name, False, "`date`,`code`")
        print("insert_db")
    except Exception as e:
        print("error :", e)
    # 重命名
    del data_new["name"]
    print(data_new)


# main函数入口
if __name__ == '__main__':
    # 计算买卖。
    tmp_datetime = common.run_with_args(stat_index_calculate)
