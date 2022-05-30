#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# apk add py-mysqldb or

import platform
import datetime
import time
import sys
import os
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR
from sqlalchemy import inspect
import pandas as pd
import traceback
import akshare as ak

# 使用环境变量获得数据库。兼容开发模式可docker模式。
MYSQL_HOST = os.environ.get('MYSQL_HOST') if (os.environ.get('MYSQL_HOST') != None) else "mysqldb"
MYSQL_USER = os.environ.get('MYSQL_USER') if (os.environ.get('MYSQL_USER') != None) else "root"
MYSQL_PWD = os.environ.get('MYSQL_PWD') if (os.environ.get('MYSQL_PWD') != None) else "mysqldb"
MYSQL_DB = os.environ.get('MYSQL_DB') if (os.environ.get('MYSQL_DB') != None) else "stock_data"

print("MYSQL_HOST :", MYSQL_HOST, ",MYSQL_USER :", MYSQL_USER, ",MYSQL_DB :", MYSQL_DB)
MYSQL_CONN_URL = "mysql+mysqldb://" + MYSQL_USER + ":" + MYSQL_PWD + "@" + MYSQL_HOST + ":3306/" + MYSQL_DB + "?charset=utf8mb4"
print("MYSQL_CONN_URL :", MYSQL_CONN_URL)

__version__ = "2.0.0"
# 每次发布时候更新。

def engine():
    engine = create_engine(
        MYSQL_CONN_URL,
        encoding='utf8', convert_unicode=True)
    return engine

def engine_to_db(to_db):
    MYSQL_CONN_URL_NEW = "mysql+mysqldb://" + MYSQL_USER + ":" + MYSQL_PWD + "@" + MYSQL_HOST + ":3306/" + to_db + "?charset=utf8mb4"
    engine = create_engine(
        MYSQL_CONN_URL_NEW,
        encoding='utf8', convert_unicode=True)
    return engine

# 通过数据库链接 engine。
def conn():
    try:
        db = pymysql.connect(host=MYSQL_HOST, port=3306, user=MYSQL_USER, password=MYSQL_PWD, db=MYSQL_DB, charset="utf8")
        # db.autocommit = True
    except Exception as e:
        print("conn error :", e)
    db.autocommit(True)
    return db.cursor()


# 定义通用方法函数，插入数据库表，并创建数据库主键，保证重跑数据的时候索引唯一。
def insert_db(data, table_name, write_index, primary_keys):
    # 插入默认的数据库。
    insert_other_db(MYSQL_DB, data, table_name, write_index, primary_keys)


# 增加一个插入到其他数据库的方法。
def insert_other_db(to_db, data, table_name, write_index, primary_keys):
    # 定义engine
    engine_mysql = engine_to_db(to_db)
    # 使用 http://docs.sqlalchemy.org/en/latest/core/reflection.html
    # 使用检查检查数据库表是否有主键。
    insp = inspect(engine_mysql)
    col_name_list = data.columns.tolist()
    # 如果有索引，把索引增加到varchar上面。
    if write_index:
        # 插入到第一个位置：
        col_name_list.insert(0, data.index.name)
    print(col_name_list)
    data.to_sql(name=table_name, con=engine_mysql, schema=to_db, if_exists='append',
                dtype={col_name: NVARCHAR(length=255) for col_name in col_name_list}, index=write_index)

    # print(insp.get_pk_constraint(table_name))
    # print()
    # print(type(insp))
    # 判断是否存在主键
    if insp.get_pk_constraint(table_name)['constrained_columns'] == []:
        with engine_mysql.connect() as con:
            # 执行数据库插入数据。
            try:
                con.execute('ALTER TABLE `%s` ADD PRIMARY KEY (%s);' % (table_name, primary_keys))
            except  Exception as e:
                print("################## ADD PRIMARY KEY ERROR :", e)




# 插入数据。
def insert(sql, params=()):
    with conn() as db:
        print("insert sql:" + sql)
        try:
            db.execute(sql, params)
        except  Exception as e:
            print("error :", e)


# 查询数据
def select(sql, params=()):
    with conn() as db:
        print("select sql:" + sql)
        try:
            db.execute(sql, params)
        except  Exception as e:
            print("error :", e)
        result = db.fetchall()
        return result


# 计算数量
def select_count(sql, params=()):
    with conn() as db:
        print("select sql:" + sql)
        try:
            db.execute(sql, params)
        except  Exception as e:
            print("error :", e)
        result = db.fetchall()
        # 只有一个数组中的第一个数据
        if len(result) == 1:
            return int(result[0][0])
        else:
            return 0


# 通用函数。获得日期参数。
def run_with_args(run_fun):
    tmp_datetime_show = datetime.datetime.now()  # 修改成默认是当日执行 + datetime.timedelta()
    tmp_hour_int = int(tmp_datetime_show.strftime("%H"))
    if tmp_hour_int < 12 :
        # 判断如果是每天 中午 12 点之前运行，跑昨天的数据。
        tmp_datetime_show = (tmp_datetime_show + datetime.timedelta(days=-1))
    tmp_datetime_str = tmp_datetime_show.strftime("%Y-%m-%d %H:%M:%S.%f")
    print("\n######################### hour_int %d " % tmp_hour_int)
    str_db = "MYSQL_HOST :" + MYSQL_HOST + ", MYSQL_USER :" + MYSQL_USER + ", MYSQL_DB :" + MYSQL_DB
    print("\n######################### " + str_db + "  ######################### ")
    print("\n######################### begin run %s %s  #########################" % (run_fun, tmp_datetime_str))
    start = time.time()
    # 要支持数据重跑机制，将日期传入。循环次数
    if len(sys.argv) == 3:
        # python xxx.py 2017-07-01 10
        tmp_year, tmp_month, tmp_day = sys.argv[1].split("-")
        loop = int(sys.argv[2])
        tmp_datetime = datetime.datetime(int(tmp_year), int(tmp_month), int(tmp_day))
        for i in range(0, loop):
            # 循环插入多次数据，重复跑历史数据使用。
            # time.sleep(5)
            tmp_datetime_new = tmp_datetime + datetime.timedelta(days=i)
            try:
                run_fun(tmp_datetime_new)
            except Exception as e:
                print("error :", e)
                traceback.print_exc()
    elif len(sys.argv) == 2:
        # python xxx.py 2017-07-01
        tmp_year, tmp_month, tmp_day = sys.argv[1].split("-")
        tmp_datetime = datetime.datetime(int(tmp_year), int(tmp_month), int(tmp_day))
        try:
            run_fun(tmp_datetime)
        except Exception as e:
            print("error :", e)
            traceback.print_exc()
    else:
        # tmp_datetime = datetime.datetime.now() + datetime.timedelta(days=-1)
        try:
            run_fun(tmp_datetime_show)  # 使用当前时间
        except Exception as e:
            print("error :", e)
            traceback.print_exc()
    print("######################### finish %s , use time: %s #########################" % (
        tmp_datetime_str, time.time() - start))


# 设置基础目录，每次加载使用。
bash_stock_tmp = "/data/cache/hist_data_cache/%s/%s/"
if not os.path.exists(bash_stock_tmp):
    os.makedirs(bash_stock_tmp)  # 创建多个文件夹结构。
    print("######################### init tmp dir #########################")


# 增加读取股票缓存方法。加快处理速度。
def get_hist_data_cache(code, date_start, date_end):
    cache_dir = bash_stock_tmp % (date_end[0:7], date_end)
    # 如果没有文件夹创建一个。月文件夹和日文件夹。方便删除。
    # print("cache_dir:", cache_dir)
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    cache_file = cache_dir + "%s^%s.gzip.pickle" % (date_end, code)
    # 如果缓存存在就直接返回缓存数据。压缩方式。
    if os.path.isfile(cache_file):
        print("######### read from cache #########", cache_file)
        return pd.read_pickle(cache_file, compression="gzip")
    else:
        print("######### get data, write cache #########", code, date_start, date_end)
        stock = ak.stock_zh_a_hist(symbol= code, start_date=date_start, end_date=date_end, adjust="")
        stock.columns = ['date', 'open', 'close', 'high', 'low', 'volume', 'amount', 'amplitude', 'quote_change',
                         'ups_downs', 'turnover']
        if stock is None:
            return None
        stock = stock.sort_index(0)  # 将数据按照日期排序下。
        print(stock)
        stock.to_pickle(cache_file, compression="gzip")
        return stock
