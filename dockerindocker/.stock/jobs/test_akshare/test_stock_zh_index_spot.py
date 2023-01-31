#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import akshare as ak
import libs.common as common

print(ak.__version__)

#stock_sse_summary_df = ak.stock_sse_summary()
#print(stock_sse_summary_df)

# 接口: stock_zh_index_spot
# 目标地址: http://vip.stock.finance.sina.com.cn/mkt/#hs_s
# 描述: 中国股票指数数据, 注意该股票指数指新浪提供的国内股票指数
# 限量: 单次返回所有指数的实时行情数据
stock_zh_index_spot_df = ak.stock_zh_index_spot()
print(stock_zh_index_spot_df)

# 插入到 MySQL 数据库中
common.insert_db(stock_zh_index_spot_df, "stock_zh_index_spot_df", True, "`symbol`")
