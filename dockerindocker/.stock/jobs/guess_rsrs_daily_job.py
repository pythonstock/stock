#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


import libs.common as common
import pandas as pd
import numpy as np
import math
import datetime
import stockstats


### 对每日指标数据，进行筛选。将符合条件的。二次筛选出来。
### 只是做简单筛选
def stat_all_lite_buy(tmp_datetime):
    datetime_str = (tmp_datetime).strftime("%Y-%m-%d")
    datetime_int = (tmp_datetime).strftime("%Y%m%d")
    print("datetime_str:", datetime_str)
    print("datetime_int:", datetime_int)

    # K值在80以上，D值在70以上，J值大于90时为超买。
    # J大于100时为超买，小于10时为超卖。
    # 当六日指标上升到达80时，表示股市已有超买现象
    # 当CCI＞﹢100 时，表明股价已经进入非常态区间——超买区间，股价的异动现象应多加关注。
    sql_1 = """
            SELECT `date`, `code`, `name`, `changepercent`, `trade`, `open`, `high`, `low`, 
                            `settlement`, `volume`, `turnoverratio`, `amount`, `per`, `pb`, `mktcap`,
                             `nmc` ,`kdjj`,`rsi_6`,`cci`
                        FROM stock_data.guess_indicators_daily WHERE `date` = %s 
                        and kdjk >= 80 and kdjd >= 70 and kdjj >= 100  and rsi_6 >= 80  and cci >= 100
    """  # and kdjj > 100 and rsi_6 > 80  and cci > 100 # 调整参数，提前获得股票增长。

    try:
        # 删除老数据。
        del_sql = " DELETE FROM `stock_data`.`guess_indicators_lite_buy_daily` WHERE `date`= '%s' " % datetime_int
        common.insert(del_sql)
    except Exception as e:
        print("error :", e)

    data = pd.read_sql(sql=sql_1, con=common.engine(), params=[datetime_int])
    data = data.drop_duplicates(subset="code", keep="last")
    print("######## len data ########:", len(data))

    try:
        common.insert_db(data, "guess_indicators_lite_buy_daily", False, "`date`,`code`")
    except Exception as e:
        print("error :", e)

# 设置卖出数据。
def stat_all_lite_sell(tmp_datetime):
    datetime_str = (tmp_datetime).strftime("%Y-%m-%d")
    datetime_int = (tmp_datetime).strftime("%Y%m%d")
    print("datetime_str:", datetime_str)
    print("datetime_int:", datetime_int)

    # 超卖区：K值在20以下，D值在30以下为超卖区。一般情况下，股价有可能上涨，反弹的可能性增大。局内人不应轻易抛出股票，局外人可寻机入场。
    # J大于100时为超买，小于10时为超卖。
    # 当六日强弱指标下降至20时，表示股市有超卖现象
    # 当CCI＜﹣100时，表明股价已经进入另一个非常态区间——超卖区间，投资者可以逢低吸纳股票。
    sql_1 = """
            SELECT `date`, `code`, `name`, `changepercent`, `trade`, `open`, `high`, `low`, 
                            `settlement`, `volume`, `turnoverratio`, `amount`, `per`, `pb`, `mktcap`,
                             `nmc` ,`kdjj`,`rsi_6`,`cci`
                        FROM stock_data.guess_indicators_daily WHERE `date` = %s 
                        and kdjk <= 20 and kdjd <= 30 and kdjj <= 10  and rsi_6 <= 20  and cci <= -100
    """

    try:
        # 删除老数据。
        del_sql = " DELETE FROM `stock_data`.`guess_indicators_lite_sell_daily` WHERE `date`= '%s' " % datetime_int
        common.insert(del_sql)
    except Exception as e:
        print("error :", e)

    data = pd.read_sql(sql=sql_1, con=common.engine(), params=[datetime_int])
    data = data.drop_duplicates(subset="code", keep="last")
    print("######## len data ########:", len(data))

    try:
        common.insert_db(data, "guess_indicators_lite_sell_daily", False, "`date`,`code`")
    except Exception as e:
        print("error :", e)

# 批处理数据。
def stat_all_batch(tmp_datetime):
    datetime_str = (tmp_datetime).strftime("%Y-%m-%d")
    datetime_int = (tmp_datetime).strftime("%Y%m%d")
    print("datetime_str:", datetime_str)
    print("datetime_int:", datetime_int)

    try:
        # 删除老数据。
        del_sql = " DELETE FROM `stock_data`.`guess_indicators_daily` WHERE `date`= %s " % datetime_int
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
        stat_index_all(data, i)


# 分批执行。
def stat_index_all(data, idx):
    # print(data["trade"])
    # 1), n天涨跌百分百计算
    # open price change (in percent) between today and the day before yesterday ‘r’ stands for rate.
    # stock[‘close_-2_r’]
    # 可以看到，-n天数据和今天数据的百分比。


    # 2), CR指标
    # http://wiki.mbalib.com/wiki/CR%E6%8C%87%E6%A0%87 价格动量指标
    # CR跌穿a、b、c、d四条线，再由低点向上爬升160时，为短线获利的一个良机，应适当卖出股票。
    # CR跌至40以下时，是建仓良机。而CR高于300~400时，应注意适当减仓。

    # 3), KDJ指标
    # http://wiki.mbalib.com/wiki/%E9%9A%8F%E6%9C%BA%E6%8C%87%E6%A0%87
    # 随机指标(KDJ)一般是根据统计学的原理，通过一个特定的周期（常为9日、9周等）内出现过的最高价、
    # 最低价及最后一个计算周期的收盘价及这三者之间的比例关系，来计算最后一个计算周期的未成熟随机值RSV，
    # 然后根据平滑移动平均线的方法来计算K值、D值与J值，并绘成曲线图来研判股票走势。
    # （3）在使用中，常有J线的指标，即3乘以K值减2乘以D值（3K－2D＝J），其目的是求出K值与D值的最大乖离程度，
    # 以领先KD值找出底部和头部。J大于100时为超买，小于10时为超卖。

    # 4), MACD指标
    # http://wiki.mbalib.com/wiki/MACD
    # 平滑异同移动平均线(Moving Average Convergence Divergence，简称MACD指标)，也称移动平均聚散指标
    # MACD 则可发挥其应有的功能，但当市场呈牛皮盘整格局，股价不上不下时，MACD买卖讯号较不明显。
    # 当用MACD作分析时，亦可运用其他的技术分析指标如短期 K，D图形作为辅助工具，而且也可对买卖讯号作双重的确认。


    # 5), BOLL指标
    # http://wiki.mbalib.com/wiki/BOLL
    # 布林线指标(Bollinger Bands)

    # 6), RSI指标
    # http://wiki.mbalib.com/wiki/RSI
    # 相对强弱指标（Relative Strength Index，简称RSI），也称相对强弱指数、相对力度指数
    # （2）强弱指标保持高于50表示为强势市场，反之低于50表示为弱势市场。
    # （3）强弱指标多在70与30之间波动。当六日指标上升到达80时，表示股市已有超买现象，
    # 如果一旦继续上升，超过90以上时，则表示已到严重超买的警戒区，股价已形成头部，极可能在短期内反转回转。


    # 7), W%R指标
    # http://wiki.mbalib.com/wiki/%E5%A8%81%E5%BB%89%E6%8C%87%E6%A0%87
    # 威廉指数（Williams%Rate）该指数是利用摆动点来度量市场的超买超卖现象。

    # 8), CCI指标
    # http://wiki.mbalib.com/wiki/%E9%A1%BA%E5%8A%BF%E6%8C%87%E6%A0%87
    # 顺势指标又叫CCI指标，其英文全称为“Commodity Channel Index”，
    # 是由美国股市分析家唐纳德·蓝伯特（Donald Lambert）所创造的，是一种重点研判股价偏离度的股市分析工具。
    # 1、当CCI指标从下向上突破﹢100线而进入非常态区间时，表明股价脱离常态而进入异常波动阶段，
    # 中短线应及时买入，如果有比较大的成交量配合，买入信号则更为可靠。
    # 　　2、当CCI指标从上向下突破﹣100线而进入另一个非常态区间时，表明股价的盘整阶段已经结束，
    # 将进入一个比较长的寻底过程，投资者应以持币观望为主。
    # CCI, default to 14 days

    # 9), TR、ATR指标
    # http://wiki.mbalib.com/wiki/%E5%9D%87%E5%B9%85%E6%8C%87%E6%A0%87
    # 均幅指标（Average True Ranger,ATR）
    # 均幅指标（ATR）是取一定时间周期内的股价波动幅度的移动平均值，主要用于研判买卖时机。

    # 10), DMA指标
    # http://wiki.mbalib.com/wiki/DMA
    # 　DMA指标（Different of Moving Average）又叫平行线差指标，是目前股市分析技术指标中的一种中短期指标，它常用于大盘指数和个股的研判。
    # DMA, difference of 10 and 50 moving average
    # stock[‘dma’]

    # 11), DMI，+DI，-DI，DX，ADX，ADXR指标
    # http://wiki.mbalib.com/wiki/DMI
    # 动向指数Directional Movement Index,DMI）
    # http://wiki.mbalib.com/wiki/ADX
    # 平均趋向指标（Average Directional Indicator，简称ADX）
    # http://wiki.mbalib.com/wiki/%E5%B9%B3%E5%9D%87%E6%96%B9%E5%90%91%E6%8C%87%E6%95%B0%E8%AF%84%E4%BC%B0
    # 平均方向指数评估（ADXR）实际是今日ADX与前面某一日的ADX的平均值。ADXR在高位与ADX同步下滑，可以增加对ADX已经调头的尽早确认。
    # ADXR是ADX的附属产品，只能发出一种辅助和肯定的讯号，并非入市的指标，而只需同时配合动向指标(DMI)的趋势才可作出买卖策略。
    # 在应用时，应以ADX为主，ADXR为辅。

    # 12), TRIX，MATRIX指标
    # http://wiki.mbalib.com/wiki/TRIX
    # TRIX指标又叫三重指数平滑移动平均指标（Triple Exponentially Smoothed Average）

    # 13), VR，MAVR指标
    # http://wiki.mbalib.com/wiki/%E6%88%90%E4%BA%A4%E9%87%8F%E6%AF%94%E7%8E%87
    # 成交量比率（Volumn Ratio，VR）（简称VR），是一项通过分析股价上升日成交额（或成交量，下同）与股价下降日成交额比值，
    # 从而掌握市场买卖气势的中期技术指标。

    stock_column = ['adx', 'adxr', 'boll', 'boll_lb', 'boll_ub', 'cci', 'cci_20', 'close_-1_r',
                    'close_-2_r', 'code', 'cr', 'cr-ma1', 'cr-ma2', 'cr-ma3', 'date', 'dma', 'dx',
                    'kdjd', 'kdjj', 'kdjk', 'macd', 'macdh', 'macds', 'mdi', 'pdi',
                    'rsi_12', 'rsi_6', 'trix', 'trix_9_sma', 'vr', 'vr_6_sma', 'wr_10', 'wr_6']
    # code     cr cr-ma1 cr-ma2 cr-ma3      date

    data_new = concat_guess_data(stock_column, data)

    data_new = data_new.round(2)  # 数据保留2位小数

    # print(data_new.head())
    print("########insert db guess_indicators_daily idx :########:", idx)
    try:
        common.insert_db(data_new, "guess_indicators_daily", False, "`date`,`code`")
    except Exception as e:
        print("error :", e)


# 链接guess 数据。
def concat_guess_data(stock_column, data):
    # 使用 trade 填充数据
    print("stock_column:", stock_column)
    tmp_dic = {}
    # 循环增加临时数据。如果要是date，和code，
    for col in stock_column:
        if col == 'date':
            tmp_dic[col] = data["date"]
        elif col == 'code':
            tmp_dic[col] = data["code"]
        else:
            tmp_dic[col] = data["trade"]
    # print("##########tmp_dic: ", tmp_dic)
    print("########################## BEGIN ##########################")
    stock_guess = pd.DataFrame(tmp_dic, index=data.index.values)
    print(stock_guess.columns.values)
    # print(stock_guess.head())
    stock_guess = stock_guess.apply(apply_guess, stock_column=stock_column, axis=1)  # , axis=1)
    print(stock_guess.head())
    # stock_guess.astype('float32', copy=False)
    stock_guess.drop('date', axis=1, inplace=True)  # 删除日期字段，然后和原始数据合并。
    # print(stock_guess["5d"])
    data_new = pd.merge(data, stock_guess, on=['code'], how='left')
    print("#############")
    return data_new


# 带参数透传。
def apply_guess(tmp, stock_column):
    # print("apply_guess columns args:", stock_column)
    # print("apply_guess data :", type(tmp))
    date = tmp["date"]
    code = tmp["code"]
    date_end = datetime.datetime.strptime(date, "%Y%m%d")
    date_start = (date_end + datetime.timedelta(days=-100)).strftime("%Y-%m-%d")
    date_end = date_end.strftime("%Y-%m-%d")
    # print(code, date_start, date_end)
    # open, high, close, low, volume, price_change, p_change, ma5, ma10, ma20, v_ma5, v_ma10, v_ma20, turnover
    # 使用缓存方法。加快计算速度。
    stock = common.get_hist_data_cache(code, date_start, date_end)
    # 设置返回数组。
    stock_data_list = []
    stock_name_list = []
    # 增加空判断，如果是空返回 0 数据。
    if stock is None:
        for col in stock_column:
            if col == 'date':
                stock_data_list.append(date)
                stock_name_list.append('date')
            elif col == 'code':
                stock_data_list.append(code)
                stock_name_list.append('code')
            else:
                stock_data_list.append(0)
                stock_name_list.append(col)
        return pd.Series(stock_data_list, index=stock_name_list)

    # print(stock.head())
    # open  high  close   low     volume
    # stock = pd.DataFrame({"close": stock["close"]}, index=stock.index.values)
    stock = stock.sort_index(0)  # 将数据按照日期排序下。

    stock["date"] = stock.index.values  # 增加日期列。
    stock = stock.sort_index(0)  # 将数据按照日期排序下。
    # print(stock) [186 rows x 14 columns]
    # 初始化统计类
    # stockStat = stockstats.StockDataFrame.retype(pd.read_csv('002032.csv'))
    stockStat = stockstats.StockDataFrame.retype(stock)

    print("########################## print result ##########################")
    for col in stock_column:
        if col == 'date':
            stock_data_list.append(date)
            stock_name_list.append('date')
        elif col == 'code':
            stock_data_list.append(code)
            stock_name_list.append('code')
        else:
            # 将数据的最后一个返回。
            tmp_val = stockStat[col].tail(1).values[0]
            if np.isinf(tmp_val):  # 解决值中存在INF问题。
                tmp_val = 0
            if np.isnan(tmp_val):  # 解决值中存在NaN问题。
                tmp_val = 0
            # print("col name : ", col, tmp_val)
            stock_data_list.append(tmp_val)
            stock_name_list.append(col)
    # print(stock_data_list)
    return pd.Series(stock_data_list, index=stock_name_list)


# print(stock["mov_vol"].tail())
# print(stock["return"].tail())
# print("stock[10d].tail(1)", stock["10d"].tail(1).values[0])
# 10d    20d  5-10d  5-20d     5d    60d    code      date  mov_vol  return
# tmp = list([stock["10d"].tail(1).values[0], stock["20d"].tail(1).values[0], stock["5-10d"].tail(1).values[0],
#             stock["5-20d"].tail(1).values[0], stock["5d"].tail(1).values[0], stock["60d"].tail(1).values[0],
#             code, date, stock["mov_vol"].tail(1).values[0], stock["return"].tail(1).values[0]])
# # print(tmp)
# return tmp


# main函数入口
if __name__ == '__main__':
    # 使用方法传递。
    tmp_datetime = common.run_with_args(stat_all_batch)
    # 二次筛选数据。直接计算买卖股票数据。
    tmp_datetime = common.run_with_args(stat_all_lite_buy)
    tmp_datetime = common.run_with_args(stat_all_lite_sell)


####################### 老方法，弃用了。#######################
def stat_index_all_no_use(tmp_datetime):
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
    data = data.drop_duplicates(subset="code", keep="last")
    print("########data[trade]########:", len(data))
    # print(data["trade"])

    # 1), n天涨跌百分百计算
    # open price change (in percent) between today and the day before yesterday ‘r’ stands for rate.
    # stock[‘close_-2_r’]
    # 可以看到，-n天数据和今天数据的百分比。
    stock_column = ['close_-1_r', 'close_-2_r', 'code', 'date']  # close_-1_r  close_-2_r    code      date
    data_new = concat_guess_data(stock_column, data)

    # 2), CR指标
    # http://wiki.mbalib.com/wiki/CR%E6%8C%87%E6%A0%87 价格动量指标
    # CR跌穿a、b、c、d四条线，再由低点向上爬升160时，为短线获利的一个良机，应适当卖出股票。
    # CR跌至40以下时，是建仓良机。而CR高于300~400时，应注意适当减仓。
    stock_column = ['code', 'cr', 'cr-ma1', 'cr-ma2', 'cr-ma3', 'date']  # code     cr cr-ma1 cr-ma2 cr-ma3      date
    data_new = concat_guess_data(stock_column, data_new)

    # 3), KDJ指标
    # http://wiki.mbalib.com/wiki/%E9%9A%8F%E6%9C%BA%E6%8C%87%E6%A0%87
    # 随机指标(KDJ)一般是根据统计学的原理，通过一个特定的周期（常为9日、9周等）内出现过的最高价、
    # 最低价及最后一个计算周期的收盘价及这三者之间的比例关系，来计算最后一个计算周期的未成熟随机值RSV，
    # 然后根据平滑移动平均线的方法来计算K值、D值与J值，并绘成曲线图来研判股票走势。
    # （3）在使用中，常有J线的指标，即3乘以K值减2乘以D值（3K－2D＝J），其目的是求出K值与D值的最大乖离程度，
    # 以领先KD值找出底部和头部。J大于100时为超买，小于10时为超卖。
    stock_column = ['code', 'date', 'kdjd', 'kdjj', 'kdjk']  # code      date   kdjd   kdjj   kdjk
    data_new = concat_guess_data(stock_column, data_new)

    # 4), MACD指标
    # http://wiki.mbalib.com/wiki/MACD
    # 平滑异同移动平均线(Moving Average Convergence Divergence，简称MACD指标)，也称移动平均聚散指标
    # MACD 则可发挥其应有的功能，但当市场呈牛皮盘整格局，股价不上不下时，MACD买卖讯号较不明显。
    # 当用MACD作分析时，亦可运用其他的技术分析指标如短期 K，D图形作为辅助工具，而且也可对买卖讯号作双重的确认。
    stock_column = ['code', 'date', 'macd', 'macdh', 'macds']  # code      date   macd  macdh  macds
    data_new = concat_guess_data(stock_column, data_new)

    # 5), BOLL指标
    # http://wiki.mbalib.com/wiki/BOLL
    # 布林线指标(Bollinger Bands)
    stock_column = ['boll', 'boll_lb', 'boll_ub', 'code', 'date']  # boll boll_lb boll_ub    code      date
    data_new = concat_guess_data(stock_column, data_new)

    # 6), RSI指标
    # http://wiki.mbalib.com/wiki/RSI
    # 相对强弱指标（Relative Strength Index，简称RSI），也称相对强弱指数、相对力度指数
    # （2）强弱指标保持高于50表示为强势市场，反之低于50表示为弱势市场。
    # （3）强弱指标多在70与30之间波动。当六日指标上升到达80时，表示股市已有超买现象，
    # 如果一旦继续上升，超过90以上时，则表示已到严重超买的警戒区，股价已形成头部，极可能在短期内反转回转。
    stock_column = ['code', 'date', 'rsi_12', 'rsi_6']  # code      date rsi_12  rsi_6
    data_new = concat_guess_data(stock_column, data_new)

    # 7), W%R指标
    # http://wiki.mbalib.com/wiki/%E5%A8%81%E5%BB%89%E6%8C%87%E6%A0%87
    # 威廉指数（Williams%Rate）该指数是利用摆动点来度量市场的超买超卖现象。
    stock_column = ['code', 'date', 'wr_10', 'wr_6']  # code      date  wr_10   wr_6
    data_new = concat_guess_data(stock_column, data_new)

    # 8), CCI指标
    # http://wiki.mbalib.com/wiki/%E9%A1%BA%E5%8A%BF%E6%8C%87%E6%A0%87
    # 顺势指标又叫CCI指标，其英文全称为“Commodity Channel Index”，
    # 是由美国股市分析家唐纳德·蓝伯特（Donald Lambert）所创造的，是一种重点研判股价偏离度的股市分析工具。
    # 1、当CCI指标从下向上突破﹢100线而进入非常态区间时，表明股价脱离常态而进入异常波动阶段，
    # 中短线应及时买入，如果有比较大的成交量配合，买入信号则更为可靠。
    # 　　2、当CCI指标从上向下突破﹣100线而进入另一个非常态区间时，表明股价的盘整阶段已经结束，
    # 将进入一个比较长的寻底过程，投资者应以持币观望为主。
    # CCI, default to 14 days
    stock_column = ['cci', 'cci_20', 'code', 'date']  # cci cci_20 code date
    data_new = concat_guess_data(stock_column, data_new)

    # 9), TR、ATR指标
    # http://wiki.mbalib.com/wiki/%E5%9D%87%E5%B9%85%E6%8C%87%E6%A0%87
    # 均幅指标（Average True Ranger,ATR）
    # 均幅指标（ATR）是取一定时间周期内的股价波动幅度的移动平均值，主要用于研判买卖时机。
    stock_column = ['cci', 'cci_20', 'code', 'date']  # cci cci_20 code date
    data_new = concat_guess_data(stock_column, data_new)

    # 10), DMA指标
    # http://wiki.mbalib.com/wiki/DMA
    # 　DMA指标（Different of Moving Average）又叫平行线差指标，是目前股市分析技术指标中的一种中短期指标，它常用于大盘指数和个股的研判。
    # DMA, difference of 10 and 50 moving average
    # stock[‘dma’]
    stock_column = ['code', 'date', 'dma']  # code    date       dma
    data_new = concat_guess_data(stock_column, data_new)

    # 11), DMI，+DI，-DI，DX，ADX，ADXR指标
    # http://wiki.mbalib.com/wiki/DMI
    # 动向指数Directional Movement Index,DMI）
    # http://wiki.mbalib.com/wiki/ADX
    # 平均趋向指标（Average Directional Indicator，简称ADX）
    # http://wiki.mbalib.com/wiki/%E5%B9%B3%E5%9D%87%E6%96%B9%E5%90%91%E6%8C%87%E6%95%B0%E8%AF%84%E4%BC%B0
    # 平均方向指数评估（ADXR）实际是今日ADX与前面某一日的ADX的平均值。ADXR在高位与ADX同步下滑，可以增加对ADX已经调头的尽早确认。
    # ADXR是ADX的附属产品，只能发出一种辅助和肯定的讯号，并非入市的指标，而只需同时配合动向指标(DMI)的趋势才可作出买卖策略。
    # 在应用时，应以ADX为主，ADXR为辅。
    stock_column = ['adx', 'adxr', 'code', 'date', 'dx', 'mdi',
                    'pdi']  # adx   adxr    code      date     dx    mdi    pdi
    data_new = concat_guess_data(stock_column, data_new)

    # 12), TRIX，MATRIX指标
    # http://wiki.mbalib.com/wiki/TRIX
    # TRIX指标又叫三重指数平滑移动平均指标（Triple Exponentially Smoothed Average）
    stock_column = ['code', 'date', 'trix', 'trix_9_sma']  # code      date    trix trix_9_sma
    data_new = concat_guess_data(stock_column, data_new)

    # 13), VR，MAVR指标
    # http://wiki.mbalib.com/wiki/%E6%88%90%E4%BA%A4%E9%87%8F%E6%AF%94%E7%8E%87
    # 成交量比率（Volumn Ratio，VR）（简称VR），是一项通过分析股价上升日成交额（或成交量，下同）与股价下降日成交额比值，
    # 从而掌握市场买卖气势的中期技术指标。
    stock_column = ['code', 'date', 'vr', 'vr_6_sma']  # code      date          vr    vr_6_sma
    data_new = concat_guess_data(stock_column, data_new)

    data_new = data_new.round(2)  # 数据保留2位小数

    # 删除老数据。
    del_sql = " DELETE FROM `stock_data`.`guess_indicators_daily` WHERE `date`= %s " % datetime_int
    common.insert(del_sql)

    # print(data_new.head())
    # data_new["down_rate"] = (data_new["trade"] - data_new["wave_mean"]) / data_new["wave_base"]
    common.insert_db(data_new, "guess_indicators_daily", False, "`date`,`code`")

    # 进行左连接.
    # tmp = pd.merge(tmp, tmp2, on=['company_id'], how='left')
