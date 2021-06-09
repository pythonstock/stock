#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import akshare as ak
import libs.common as common

print(ak.__version__)

# 实时行情数据
# 接口: stock_zh_a_spot
# 目标地址: http://vip.stock.finance.sina.com.cn/mkt/#hs_a
# 描述: A 股数据是从新浪财经获取的数据, 重复运行本函数会被新浪暂时封 IP, 建议增加时间间隔
# 限量: 单次返回所有 A 股上市公司的实时行情数据

stock_zh_a_spot_df = ak.stock_zh_a_spot()
print(stock_zh_a_spot_df)

# 插入到 MySQL 数据库中
common.insert_db(stock_zh_a_spot_df, "stock_zh_a_spot", True, "`symbol`")
