#!/usr/local/bin/python
# -*- coding: utf-8 -*-

class StockWebData:
    def __init__(self, name, table_name, columns, column_names,order_by):
        self.name = name
        self.table_name = table_name
        self.columns = columns
        self.column_names = column_names
        self.order_by = order_by


STOCK_WEB_DATA_LIST = {}

STOCK_WEB_DATA_LIST["ts_deposit_rate"] = StockWebData(
    name="存款利率",
    table_name="ts_deposit_rate",
    columns=["date", "deposit_type", "rate"],
    column_names=["日期", "存款类型", "存款利率"],
    order_by = " date desc "
)
