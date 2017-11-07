#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# apk add py-mysqldb or

import platform
import datetime
import time
import sys
import os
import MySQLdb
from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR
from sqlalchemy import inspect

# 使用环境变量获得数据库。兼容开发模式可docker模式。
MYSQL_HOST = os.environ.get('MYSQL_HOST') if (os.environ.get('MYSQL_HOST') != None) else "mariadb"
MYSQL_USER = os.environ.get('MYSQL_USER') if (os.environ.get('MYSQL_USER') != None) else "root"
MYSQL_PWD = os.environ.get('MYSQL_PWD') if (os.environ.get('MYSQL_PWD') != None) else "mariadb"
MYSQL_DB = os.environ.get('MYSQL_DB') if (os.environ.get('MYSQL_DB') != None) else "stock_data"

print("MYSQL_HOST:", MYSQL_HOST, ",MYSQL_USER:", MYSQL_USER, ",MYSQL_DB:", MYSQL_DB)


def engine():
    engine = create_engine(
        "mysql+mysqldb://" + MYSQL_USER + ":" + MYSQL_PWD + "@" + MYSQL_HOST + "/" + MYSQL_DB + "?charset=utf8",
        encoding='utf8', convert_unicode=True)
    return engine


def conn():
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PWD, MYSQL_DB, charset="utf8")
    # db.autocommit(on=True)
    return db


# 定义通用方法函数，插入数据库表，并创建数据库主键，保证重跑数据的时候索引唯一。
def insert_db(data, table_name, write_index, primary_keys):
    # 定义engine
    engine_mysql = engine()
    # 使用 http://docs.sqlalchemy.org/en/latest/core/reflection.html
    # 使用检查检查数据库表是否有主键。
    insp = inspect(engine_mysql)
    col_name_list = data.columns.tolist()
    # 如果有索引，把索引增加到varchar上面。
    if write_index:
        # 插入到第一个位置：
        col_name_list.insert(0, data.index.name)
    print(col_name_list)
    data.to_sql(name=table_name, con=engine_mysql, schema=MYSQL_DB, if_exists='append',
                dtype={col_name: NVARCHAR(length=255) for col_name in col_name_list}, index=write_index)
    # 判断是否存在主键
    if insp.get_primary_keys(table_name) == []:
        with engine_mysql.connect() as con:
            # 执行数据库插入数据。
            try:
                con.execute('ALTER TABLE `%s` ADD PRIMARY KEY (%s);' % (table_name, primary_keys))
            except  Exception as e:
                print("################## ADD PRIMARY KEY ERROR :", e)


# 插入数据。
def insert(sql):
    with conn() as db:
        print("insert sql:" + sql)
        try:
            db.execute(sql)
        except  Exception as e:
            print("error :", e)


# 查询数据
def select(sql):
    with conn() as db:
        print("select sql:" + sql)
        try:
            db.execute(sql)
        except  Exception as e:
            print("error :", e)
        result = db.fetchall()
        return result


# 计算数量
def select_count(sql):
    with conn() as db:
        print("select sql:" + sql)
        try:
            db.execute(sql)
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
    tmp_datetime_str = tmp_datetime_show.strftime("%Y-%m-%d %H:%M:%S.%f")
    print("\n\n######################### begin run %s  #########################" % tmp_datetime_str)
    start = time.time()
    # 要支持数据重跑机制，将日期传入。循环次数
    if len(sys.argv) == 3:
        # python xxx.py 2017-07-01 10
        tmp_year, tmp_month, tmp_day = sys.argv[1].split("-")
        loop = int(sys.argv[2])
        tmp_datetime = datetime.datetime(int(tmp_year), int(tmp_month), int(tmp_day))
        for i in range(0, loop):
            # 循环插入多次数据，重复跑历史数据使用。
            tmp_datetime_new = tmp_datetime + datetime.timedelta(days=i)
            run_fun(tmp_datetime_new)
    elif len(sys.argv) == 2:
        # python xxx.py 2017-07-01
        tmp_year, tmp_month, tmp_day = sys.argv[1].split("-")
        tmp_datetime = datetime.datetime(int(tmp_year), int(tmp_month), int(tmp_day))
        run_fun(tmp_datetime)
    else:
        tmp_datetime = datetime.datetime.now() + datetime.timedelta(days=-1)
        run_fun(tmp_datetime)
    print("######################### finish %s , use time: %s #########################" % (
        tmp_datetime_str, time.time() - start))
