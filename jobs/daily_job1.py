#!/usr/local/bin/python
# -*- coding: utf-8 -*-


import libs.common as common
import sys
import time
import pandas as pd
import tushare as ts
from sqlalchemy.types import NVARCHAR
from sqlalchemy import inspect
import datetime

#定义通用方法函数，插入数据库表，并创建数据库主键，保证重跑数据的时候索引唯一。
def insert_db(data, table_name, primary_keys):
    # 定义engine
    engine = common.engine()
    # 使用 http://docs.sqlalchemy.org/en/latest/core/reflection.html
    # 使用检查检查数据库表是否有主键。
    insp = inspect(engine)
    data.to_sql(name=table_name, con=engine, schema=common.MYSQL_DB, if_exists='append',
                dtype={col_name: NVARCHAR(length=255) for col_name in data.columns.tolist()}, index=False)
    # 判断是否存在主键
    if insp.get_primary_keys(table_name) == []:
        with engine.connect() as con:
            # 执行数据库插入数据。
            con.execute('ALTER TABLE `%s` ADD PRIMARY KEY (%s);' % (table_name, primary_keys))


####### 3.pdf 方法。宏观经济数据
def stat_all(tmp_datetime):
    # 存款利率
    data = ts.get_deposit_rate()
    insert_db(data, "ts_deposit_rate", "`date`,`deposit_type`")

    # 贷款利率
    data = ts.get_loan_rate()
    insert_db(data, "ts_loan_rate", "`date`,`loan_type`")

    # 存款准备金率
    data = ts.get_rrr()
    insert_db(data, "ts_rrr", "`date`")

    # 货币供应量
    data = ts.get_money_supply()
    insert_db(data, "ts_money_supply", "`month`")

    # 货币供应量(年底余额)
    data = ts.get_money_supply_bal()
    insert_db(data, "ts_money_supply_bal", "`year`")

    # 国内生产总值(年度)
    data = ts.get_gdp_year()
    insert_db(data, "ts_gdp_year", "`year`")

    # 国内生产总值(季度)
    data = ts.get_gdp_quarter()
    insert_db(data, "ts_get_gdp_quarter", "`quarter`")

    # 三大需求对GDP贡献
    data = ts.get_gdp_for()
    insert_db(data, "ts_gdp_for", "`year`")

    # 三大产业对GDP拉动
    data = ts.get_gdp_pull()
    insert_db(data, "ts_gdp_pull", "`year`")

    # 三大产业贡献率
    data = ts.get_gdp_contrib()
    insert_db(data, "ts_gdp_contrib", "`year`")

    # 居民消费价格指数
    data = ts.get_cpi()
    insert_db(data, "ts_cpi", "`month`")

    # 工业品出厂价格指数
    data = ts.get_ppi()
    insert_db(data, "ts_ppi", "`month`")


# main函数入口
if __name__ == '__main__':
    # 使用方法传递。
    tmp_datetime = common.run_with_args(stat_all)
