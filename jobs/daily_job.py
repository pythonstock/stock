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


####### 使用 5.pdf，先做 基本面数据 的数据，然后在做交易数据。
#
def stat_all(tmp_datetime):
    print()


# main函数入口
if __name__ == '__main__':
    # 使用方法传递。
    tmp_datetime = common.run_with_args(stat_all)
