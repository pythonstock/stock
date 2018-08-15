#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


import libs.common as common
import pandas as pd
import numpy as np
import math
import datetime
import heapq


### 对每日指标数据，进行筛选。将符合条件的。二次筛选出来。
def stat_all_lite(tmp_datetime):
    # 要操作的数据库表名称。
    table_name = "guess_indicators_lite_buy_daily"
    datetime_str = (tmp_datetime).strftime("%Y-%m-%d")
    datetime_int = (tmp_datetime).strftime("%Y%m%d")
    print("datetime_str:", datetime_str)
    print("datetime_int:", datetime_int)

    # try:
    #     # 删除老数据。guess_indicators_lite_buy_daily 是一张单表，没有日期字段。
    #     del_sql = " DELETE FROM `stock_data`.`%s` WHERE `date`= '%s' " % (table_name, datetime_int)
    #     print("del_sql:", del_sql)
    #     common.insert(del_sql)
    #     print("del_sql")
    # except Exception as e:
    #     print("error :", e)

    sql_1 = """
                SELECT `date`, `code`, `name`, `changepercent`, `trade`,`turnoverratio`, `pb` ,`kdjj`,`rsi_6`,`cci`
                            FROM stock_data.guess_indicators_lite_daily WHERE `date` = %s 
                            and `changepercent` > 2 and `pb` > 0 
        """
    # and `changepercent` > 2 and `pb` > 0 and `turnoverratio` > 5 去除掉换手率参数。
    data = pd.read_sql(sql=sql_1, con=common.engine(), params=[datetime_int])
    data = data.drop_duplicates(subset="code", keep="last")
    print("######## len data ########:", len(data))
    # del data["name"]
    # print(data)
    data["trade_float32"] = data["trade"].astype('float32', copy=True)
    # 输入 date 用作历史数据查询。
    stock_merge = pd.DataFrame({
        "date": data["date"], "code": data["code"], "wave_mean": data["trade"],
        "wave_crest": data["trade"], "wave_base": data["trade"]}, index=data.index.values)
    print(stock_merge.head(1))

    stock_merge = stock_merge.apply(apply_merge, axis=1)  # , axis=1)
    del stock_merge["date"]  # 合并前删除 date 字段。
    # 合并数据
    data_new = pd.merge(data, stock_merge, on=['code'], how='left')

    # 使用 trade_float32 参加计算。
    data_new = data_new[data_new["trade_float32"] > data_new["wave_base"]]  # 交易价格大于波谷价格。
    data_new = data_new[data_new["trade_float32"] < data_new["wave_crest"]]  # 小于波峰价格

    # wave_base  wave_crest  wave_mean
    data_new["wave_base"] = data_new["wave_base"].round(2)  # 数据保留2位小数
    data_new["wave_crest"] = data_new["wave_crest"].round(2)  # 数据保留2位小数
    data_new["wave_mean"] = data_new["wave_mean"].round(2)  # 数据保留2位小数

    data_new["up_rate"] = (data_new["wave_mean"].sub(data_new["trade_float32"])).div(data_new["wave_crest"]).mul(100)
    data_new["up_rate"] = data_new["up_rate"].round(2)  # 数据保留2位小数

    data_new["buy"] = 1
    data_new["sell"] = 0
    data_new["today_trade"] = data_new["trade"]
    data_new["income"] = 0
    # 重命名 date
    data_new.columns.values[0] = "buy_date"
    del data_new["trade_float32"]

    try:
        common.insert_db(data_new, table_name, False, "`code`")
        print("insert_db")
    except Exception as e:
        print("error :", e)
    # 重命名
    del data_new["name"]
    print(data_new)


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
        return list([code, date, 0, 0, 0])

    stock = pd.DataFrame({"close": stock["close"]}, index=stock.index.values)
    stock = stock.sort_index(0)  # 将数据按照日期排序下。

    # print(stock.head(10))
    arr = pd.Series(stock["close"].values)
    # print(df_arr)
    wave_mean = arr.mean()
    max_point = 3  # 获得最高的几个采样点。
    # 计算股票的波峰值。
    wave_crest = heapq.nlargest(max_point, enumerate(arr), key=lambda x: x[1])
    wave_crest_mean = pd.DataFrame(wave_crest).mean()

    # 输出元祖第一个元素是index，第二元素是比较的数值 计算数据的波谷值
    wave_base = heapq.nsmallest(max_point, enumerate(arr), key=lambda x: x[1])
    wave_base_mean = pd.DataFrame(wave_base).mean()
    # 输出数据
    print("##############", len(stock))
    if len(stock) > 180:
        #     code      date wave_base wave_crest wave_mean 顺序必须一致。返回的是行数据，然后填充。
        return list([code, date, wave_base_mean[1], wave_crest_mean[1], wave_mean])
    else:
        return list([code, date, 0, 0, 0])


# main函数入口
if __name__ == '__main__':
    # 二次筛选数据。
    tmp_datetime = common.run_with_args(stat_all_lite)
