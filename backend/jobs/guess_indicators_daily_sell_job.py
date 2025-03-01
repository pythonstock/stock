#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


import libs.common as common
import pandas as pd
import numpy as np
import math
import datetime
import stockstats
from sqlalchemy import text

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
    sql_1 = text("""
            SELECT `date`,`code`,`name`,`last_price`,`change_percent`,`change_amount`,`volume`,`turnover`,
                            `amplitude`,`high`,`low`,`open`,`closed`,`volume_ratio`,`turnover_rate`,
                            `pe_ratio`,`pb_ratio`,`market_cap`,`circulating_market_cap`,`rise_speed`,
                            `change_5min`,`change_ercent_60day`,`ytd_change_percent`,
         `boll`, `boll_lb`, `boll_ub`, `kdjd`, `kdjj`, `kdjk`, `macd`, `macdh`,
         `macds`, `pdi`,`trix`, `trix_9_sma`, `vr`, `vr_6_sma`, `wr_10`, `wr_6` 
                        FROM stock_data.guess_indicators_daily WHERE `date` = :datetime
                        and kdjk <= 20 and kdjd <= 30 and kdjj <= 10  
    """)

    try:
        # 删除老数据。
        del_sql = " DELETE FROM `stock_data`.`guess_indicators_lite_sell_daily` WHERE `date`= '%s' " % datetime_int
        common.insert(del_sql)
    except Exception as e:
        print("error :", e)

    # 查询参数
    params = {"datetime": datetime_int}
    print(sql_1)
    data = pd.read_sql(sql=sql_1, con=common.engine(), params=params)
    data = data.drop_duplicates(subset="code", keep="last")
    print("######## stat_all_lite_sell len data ########:", len(data))

    try:
        common.insert_db(data, "guess_indicators_lite_sell_daily", False, "`date`,`code`")
    except Exception as e:
        print("error :", e)



# main函数入口
if __name__ == '__main__':
    # 使用方法传递。
    # 二次筛选数据。直接计算买卖股票数据。
    tmp_datetime = common.run_with_args(stat_all_lite_sell)

