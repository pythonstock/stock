#!/usr/local/bin/python
# -*- coding: utf-8 -*-

class StockWebData:
    def __init__(self, name, table_name, columns, column_names, order_by):
        self.name = name
        self.table_name = table_name
        self.columns = columns
        self.column_names = column_names
        self.order_by = order_by
        self.url = "/stock/data?name=" + self.table_name


STOCK_WEB_DATA_LIST = []

STOCK_WEB_DATA_LIST.append(
    StockWebData(
        name="存款利率",
        table_name="ts_deposit_rate",
        columns=["date", "deposit_type", "rate"],
        column_names=["日期", "存款类型", "存款利率"],
        order_by=" date desc "
    )
)

STOCK_WEB_DATA_LIST.append(
    StockWebData(
        name="贷款利率",
        table_name="ts_loan_rate",
        columns=["date", "loan_type", "rate"],
        column_names=["日期", "贷款类型", "存款利率"],
        order_by=" date desc "
    )
)

STOCK_WEB_DATA_LIST.append(
    StockWebData(
        name="存款准备金率",
        table_name="ts_rrr",
        columns=["date", "before", "now", "changed"],
        column_names=["变动日期", "调整前存款准备金率(%)", "调整后存款准备金率(%)", "调整幅度(%)"],
        order_by=" date desc "
    )
)

STOCK_WEB_DATA_LIST.append(
    StockWebData(
        name="货币供应量",
        table_name="ts_money_supply",
        columns=["month", "m2", "m2_yoy", "m1", "m1_yoy", "m0", "m0_yoy", "cd", "cd_yoy", "qm", "qm_yoy", "ftd",
                 "ftd_yoy", "sd", "sd_yoy", "rests", "rests_yoy"],
        column_names=["统计时间", "货币和准货币(广义货币M2)(亿元)", "货币和准货币(广义货币M2)同比增长(%)",
                      "货币(狭义货币M1)(亿元)", "货币(狭义货币M1)同比增长(%)",
                      "流通中现金(M0)(亿元)", "流通中现金(M0)同比增长(%)",
                      "活期存款(亿元)", "活期存款同比增长(%)",
                      "准货币(亿元)", "准货币同比增长(%)",
                      "定期存款(亿元)", "定期存款同比增长(%)",
                      "储蓄存款(亿元)", "储蓄存款同比增长(%)",
                      "其他存款(亿元)", "其他存款同比增长(%)"
                      ],
        order_by=" month desc "
    )
)

STOCK_WEB_DATA_MAP = {}
# 再拼接成Map使用。
for tmp in STOCK_WEB_DATA_LIST:
    STOCK_WEB_DATA_MAP[tmp.table_name] = tmp
    if len(tmp.columns) != len(tmp.column_names):
        print(u"error:", tmp.table_name, ",columns:", len(tmp.columns), ",column_names:", len(tmp.column_names))
