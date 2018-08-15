#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


import libs.common as common
import pandas as pd
import numpy as np
import math
import datetime
import sklearn as skl
from sklearn import datasets, linear_model
# https://github.com/udacity/machine-learning/issues/202
# sklearn.cross_validation 这个包不推荐使用了。
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier

# 要操作的数据库表名称。
table_name = "guess_sklearn_ma_daily"


# 批处理数据。
def stat_all_batch(tmp_datetime):
    datetime_str = (tmp_datetime).strftime("%Y-%m-%d")
    datetime_int = (tmp_datetime).strftime("%Y%m%d")
    print("datetime_str:", datetime_str)
    print("datetime_int:", datetime_int)

    try:
        # 删除老数据。
        del_sql = " DELETE FROM `stock_data`.`%s` WHERE `date`= %s " % (table_name, datetime_int)
        print("del_sql:", del_sql)
        common.insert(del_sql)
    except Exception as e:
        print("error :", e)

    sql_count = """
            SELECT count(1) FROM stock_data.ts_today_all WHERE `date` = %s and `trade` > 0 and `open` > 0 and trade <= 20 
                 and `code` not like %s and `name` not like %s 
    """
    # 修改逻辑，增加中小板块计算。 中小板：002，创业板：300 。and `code` not like %s and `code` not like %s and `name` not like %s
    # count = common.select_count(sql_count, params=[datetime_int, '002%', '300%', '%st%'])
    count = common.select_count(sql_count, params=[datetime_int, '300%', '%st%'])
    print("count :", count)
    batch_size = 100
    end = int(math.ceil(float(count) / batch_size) * batch_size)
    print(end)
    # for i in range(0, end, batch_size):
    for i in range(0, end, batch_size):
        print("loop :", i)
        # 查询今日满足股票数据。剔除数据：创业板股票数据，中小板股票数据，所有st股票
        # #`code` not like '002%' and `code` not like '300%'  and `name` not like '%st%'
        sql_1 = """ 
                    SELECT `date`, `code`, `name`, `changepercent`, `trade`, `open`, `high`, `low`, 
                        `settlement`, `volume`, `turnoverratio`, `amount`, `per`, `pb`, `mktcap`, `nmc` 
                    FROM stock_data.ts_today_all WHERE `date` = %s and `trade` > 0 and `open` > 0 and trade <= 20 
                        and `code` not like %s and `name` not like %s limit %s , %s
                    """
        print(sql_1)
        # data = pd.read_sql(sql=sql_1, con=common.engine(), params=[datetime_int, '002%', '300%', '%st%', i, batch_size])
        data = pd.read_sql(sql=sql_1, con=common.engine(), params=[datetime_int, '300%', '%st%', i, batch_size])
        data = data.drop_duplicates(subset="code", keep="last")
        print("########data[trade]########:", len(data))

        # 使用 trade 填充数据
        stock_sklearn = pd.DataFrame({
            "date": data["date"], "code": data["code"], "next_close": data["trade"],
            "sklearn_score": data["trade"]}, index=data.index.values)
        print(stock_sklearn.head())
        stock_sklearn_apply = stock_sklearn.apply(apply_sklearn, axis=1)  # , axis=1)
        # 重命名
        del stock_sklearn_apply["date"]  # 合并前删除 date 字段。
        # 合并数据
        data_new = pd.merge(data, stock_sklearn_apply, on=['code'], how='left')
        # for index, row in data.iterrows():
        #     next_stock, score = stat_index_all(row, i)
        #     print(next_stock, score)
        data_new["next_close"] = data_new["next_close"].round(2)  # 数据保留4位小数
        data_new["sklearn_score"] = data_new["sklearn_score"].round(2)  # 数据保留2位小数

        data_new["trade_float32"] = data["trade"].astype('float32', copy=False)
        data_new["up_rate"] = (data_new["next_close"] - data_new["trade_float32"]) * 100 / data_new["trade_float32"]
        data_new["up_rate"] = data_new["up_rate"].round(2)  # 数据保留2位小数
        del data_new["trade_float32"]

        try:
            common.insert_db(data_new, table_name, False, "`date`,`code`")
            print("insert_db")
        except Exception as e:
            print("error :", e)
        # 重命名
        del data_new["name"]
        print(data_new)


# code date next_close sklearn_score
def apply_sklearn(data):
    # 要操作的数据库表名称。
    print("########stat_index_all########:", len(data))
    date = data["date"]
    code = data["code"]
    print(date, code)
    date_end = datetime.datetime.strptime(date, "%Y%m%d")
    date_start = (date_end + datetime.timedelta(days=-300)).strftime("%Y-%m-%d")
    date_end = date_end.strftime("%Y-%m-%d")
    print(code, date_start, date_end)

    # open high close low volume price_change p_change ma5 ma10 ma20 v_ma5 v_ma10 v_ma20 turnover
    stock_X = common.get_hist_data_cache(code, date_start, date_end)
    # 增加空判断，如果是空返回 0 数据。
    if stock_X is None:
        return list([code, date, 0.0, 0.0])

    stock_X = stock_X.sort_index(0)  # 将数据按照日期排序下。
    stock_y = pd.Series(stock_X["close"].values)  # 标签

    stock_X_next = stock_X.iloc[len(stock_X) - 1]
    print("########################### stock_X_next date:", stock_X_next)
    # 使用今天的交易价格，13 个指标预测明天的价格。偏移股票数据，今天的数据，目标是明天的价格。
    stock_X = stock_X.drop(stock_X.index[len(stock_X) - 1])  # 删除最后一条数据
    stock_y = stock_y.drop(stock_y.index[0])  # 删除第一条数据
    # print("########################### stock_X date:", stock_X)

    # 删除掉close 也就是收盘价格。
    del stock_X["close"]
    del stock_X_next["close"]

    model = linear_model.LinearRegression()
    # model = KNeighborsClassifier()

    model.fit(stock_X.values, stock_y)
    # print("############## test & target #############")
    # print("############## coef_ & intercept_ #############")
    # print(model.coef_)  # 系数
    # print(model.intercept_)  # 截断
    next_close = model.predict([stock_X_next.values])
    if len(next_close) == 1:
        next_close = next_close[0]
    sklearn_score = model.score(stock_X.values, stock_y)
    print("score:", sklearn_score)  # 评分
    return list([code, date, next_close, sklearn_score * 100])


# main函数入口
if __name__ == '__main__':
    # 使用方法传递。
    tmp_datetime = common.run_with_args(stat_all_batch)
