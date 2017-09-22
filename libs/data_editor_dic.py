#!/usr/local/bin/python
# -*- coding: utf-8 -*-

class DataEditorDic:
    def __init__(self, type, name, table_name, columns, column_names, order_by):
        self.type = type
        self.name = name
        self.table_name = table_name
        self.columns = columns
        self.column_names = column_names
        self.order_by = order_by
        self.url = "/data/editor?name=" + self.table_name


DATA_EDITOR_LIST = []

DATA_EDITOR_LIST.append(
    DataEditorDic(
        type="股票配置管理",
        name="持仓管理",
        table_name="user_stock",
        columns=["code", "date", "price", "shares", "commission_rate", "tax_rate", "comment"],
        column_names=["股票代码", "日期", "价格", "数量", "佣金", "税率", "备注"],
        order_by=" code desc "
    )
)

DATA_EDITOR_MAP = {}
# 再拼接成Map使用。
for tmp in DATA_EDITOR_LIST:
    DATA_EDITOR_MAP[tmp.table_name] = tmp
    if len(tmp.columns) != len(tmp.column_names):
        print(u"error:", tmp.table_name, ",columns:", len(tmp.columns), ",column_names:", len(tmp.column_names))
