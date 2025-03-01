#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


import libs.common as common
import pandas as pd
import numpy as np
import math
import datetime
import stockstats
from sqlalchemy import text


### 对每日指标数据，进行筛选。将符合条件的。二次筛选出来。
### 只是做简单筛选
def stat_all_lite_buy(tmp_datetime):
    datetime_str = (tmp_datetime).strftime("%Y-%m-%d")
    datetime_int = (tmp_datetime).strftime("%Y%m%d")
    print("datetime_str:", datetime_str)
    print("datetime_int:", datetime_int)

    # 查询参数
    params = {"datetime": datetime_int}

    sql_kdjk = text(" SELECT avg(`kdjk`) as avg_kdjk FROM  guess_indicators_daily  ")
    data_kdjk  = pd.read_sql(sql=sql_kdjk, con=common.engine(), params=params)
    kdjk = data_kdjk["avg_kdjk"][0]

    sql_kdjd = text(" SELECT avg(`kdjd`) as avg_kdjd FROM  guess_indicators_daily  ")
    data_kdjd  = pd.read_sql(sql=sql_kdjd, con=common.engine(), params=params)
    kdjd = data_kdjd["avg_kdjd"][0]

    sql_kdjj = text(" SELECT avg(`kdjj`) as avg_kdjj FROM  guess_indicators_daily  ")
    data_kdjj  = pd.read_sql(sql=sql_kdjj, con=common.engine(), params=params)
    kdjj = data_kdjj["avg_kdjj"][0]

    # K值在80以上，D值在70以上，J值大于90时为超买。
    # J大于100时为超买，小于10时为超卖。
    # 当六日指标上升到达80时，表示股市已有超买现象
    # 当CCI＞﹢100 时，表明股价已经进入非常态区间——超买区间，股价的异动现象应多加关注。
    params_1 = {"datetime": datetime_int, "kdjk": kdjk, "kdjd": kdjd, "kdjj": kdjj}
    sql_1 = text("""
            SELECT `date`,`code`,`name`,`last_price`,`change_percent`,`change_amount`,`volume`,`turnover`,
                            `amplitude`,`high`,`low`,`open`,`closed`,`volume_ratio`,`turnover_rate`,
                            `pe_ratio`,`pb_ratio`,`market_cap`,`circulating_market_cap`,`rise_speed`,
                            `change_5min`,`change_ercent_60day`,`ytd_change_percent`,
         `boll`, `boll_lb`, `boll_ub`, `kdjd`, `kdjj`, `kdjk`, `macd`, `macdh`,
         `macds`, `pdi`,`trix`, `trix_9_sma`, `vr`, `vr_6_sma`, `wr_10`, `wr_6`     
        FROM stock_data.guess_indicators_daily WHERE `date` = :datetime
                        and kdjk >= :kdjk and kdjd >= :kdjd and kdjj >= :kdjj  
    """)  # and kdjj > 100 and rsi_6 > 80  and cci > 100 # 调整参数，提前获得股票增长。

    try:
        # 删除老数据。
        del_sql = " DELETE FROM `stock_data`.`guess_indicators_lite_buy_daily` WHERE `date`= '%s' " % datetime_int
        common.insert(del_sql)
    except Exception as e:
        print("error :", e)
    
    print(f"sql_1 : {sql_1}")
    data = pd.read_sql(sql=sql_1, con=common.engine(), params=params_1)
    data = data.drop_duplicates(subset="code", keep="last")
    print("######## stat_all_lite_buy len data ########:", len(data))

    try:
        common.insert_db(data, "guess_indicators_lite_buy_daily", False, "`date`,`code`")
    except Exception as e:
        print("error :", e)



# main函数入口
if __name__ == '__main__':
    # 使用方法传递。
    # 二次筛选数据。直接计算买卖股票数据。
    tmp_datetime = common.run_with_args(stat_all_lite_buy)

