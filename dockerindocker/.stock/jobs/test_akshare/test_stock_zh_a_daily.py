#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import akshare as ak
import libs.common as common

print(ak.__version__)

# 历史行情数据
# 日频率
# 接口: stock_zh_a_daily
# 目标地址: https://finance.sina.com.cn/realstock/company/sh600006/nc.shtml(示例)
# 描述: A 股数据是从新浪财经获取的数据, 历史数据按日频率更新; 注意其中的 sh689009 为 CDR, 请 通过 stock_zh_a_cdr_daily 接口获取
# 限量: 单次返回指定 A 股上市公司指定日期间的历史行情日频率数据
# adjust=""; 默认为空: 返回不复权的数据; qfq: 返回前复权后的数据; hfq: 返回后复权后的数据;

stock_zh_a_daily_qfq_df = ak.stock_zh_a_daily(symbol="sz000002", adjust="")
print(stock_zh_a_daily_qfq_df)

stock_zh_a_daily_qfq_df = ak.stock_zh_a_daily(symbol="sz000002", start_date="20200101", end_date="20210101", adjust="")
print(stock_zh_a_daily_qfq_df)

# 插入到 MySQL 数据库中
common.insert_db(stock_zh_a_daily_qfq_df, "stock_zh_a_daily", True, "`symbol`")



