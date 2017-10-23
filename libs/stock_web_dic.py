#!/usr/local/bin/python
# -*- coding: utf-8 -*-

class StockWebData:
    def __init__(self, mode, type, name, table_name, columns, column_names, primary_key, order_by):
        self.mode = mode  # 模式，query，editor 查询和编辑模式
        self.type = type
        self.name = name
        self.table_name = table_name
        self.columns = columns
        self.column_names = column_names
        self.primary_key = primary_key
        self.order_by = order_by
        if mode == "query":
            self.url = "/stock/data?table_name=" + self.table_name
        elif mode == "editor":
            self.url = "/data/editor?table_name=" + self.table_name


STOCK_WEB_DATA_LIST = []

STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="宏观经济数据",
        name="存款利率",
        table_name="ts_deposit_rate",
        columns=["date", "deposit_type", "rate"],
        column_names=["日期", "存款类型", "存款利率"],
        primary_key=[],
        order_by=" date desc "
    )
)

STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="宏观经济数据",
        name="贷款利率",
        table_name="ts_loan_rate",
        columns=["date", "loan_type", "rate"],
        column_names=["日期", "贷款类型", "存款利率"],
        primary_key=[],
        order_by=" date desc "
    )
)

STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="宏观经济数据",
        name="存款准备金率",
        table_name="ts_rrr",
        columns=["date", "before", "now", "changed"],
        column_names=["变动日期", "调整前存款准备金率(%)", "调整后存款准备金率(%)", "调整幅度(%)"],
        primary_key=[],
        order_by=" date desc "
    )
)

STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="宏观经济数据",
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
        primary_key=[],
        order_by=" month desc "
    )
)

# http://tushare.org/fundamental.html
# 参考官网网站的文档，是最全的。
STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="基本面数据",
        name="股票列表",
        table_name="ts_stock_basics",
        columns=["code", "name", "industry", "area", "pe", "outstanding", "totals", "totalAssets", "liquidAssets",
                 "fixedAssets", "reserved", "reservedPerShare", "esp", "bvps", "pb", "timeToMarket",
                 "undp", "perundp", "rev", "profit", "gpr", "npr", "holders"],
        column_names=["代码", "名称", "所属行业", "地区", "市盈率", "流通股本(亿)", "总股本(亿)", "总资产(万)", "流动资产",
                      "固定资产", "公积金", "每股公积金", "每股收益", "每股净资", "市净率", "上市日期", "未分利润",
                      "每股未分配", "收入同比(%)", "利润同比(%)", "毛利率(%)", "净利润率(%)", "股东人数"
                      ],
        primary_key=[],
        order_by=" code asc "
    )
)

# 业绩报告（主表）
STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="基本面数据",
        name="业绩报告（主表）",
        table_name="ts_report_data",
        columns=["quarter", "code", "name", "eps", "eps_yoy", "bvps", "roe", "epcf", "net_profits",
                 "profits_yoy", "distrib", "report_date"],
        column_names=["季度", "代码", "名称", "每股收益", "每股收益同比(%)", "每股净资产", "净资产收益率(%)", "每股现金流量(元)", ",净利润(万元)",
                      "净利润同比(%)", "分配方案", "发布日期"
                      ],
        primary_key=[],
        order_by=" quarter desc "
    )
)

# 盈利能力
STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="基本面数据",
        name="盈利能力",
        table_name="ts_profit_data",
        columns=["quarter", "code", "name", "roe", "net_profit_ratio", "gross_profit_rate",
                 "net_profits", "eps", "business_income", "bips"],
        column_names=["季度", "代码", "名称", "净资产收益率(%)", "净利率(%)", "毛利率(%)", "净利润(万元)",
                      "每股收益", "营业收入(百万元)", "每股主营业务收入(元)"],
        primary_key=[],
        order_by=" quarter desc "
    )
)

STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="基本面数据",
        name="营运能力",
        table_name="ts_operation_data",
        columns=["quarter", "code", "name", "arturnover", "arturndays",
                 "inventory_turnover", "inventory_days", "currentasset_turnover", "currentasset_days"],
        column_names=["季度", "代码", "名称", "应收账款周转率(次)", "应收账款周转天数(天)", "存货周转率(次)", "存货周转天数(天)",
                      "流动资产周转率(次)", "流动资产周转天数(天)"
                      ],
        primary_key=[],
        order_by=" quarter desc "
    )
)

STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="基本面数据",
        name="成长能力",
        table_name="ts_growth_data",
        columns=["quarter", "code", "name", "mbrg", "nprg", "nav", "targ", "epsg", "seg"],
        column_names=["季度", "代码", "名称", "主营业务收入增长率(%)", "净利润增长率(%)", "净资产增长率", "总资产增长率",
                      "每股收益增长率", "股东权益增长率"],
        primary_key=[],
        order_by=" quarter desc  "
    )
)

# "code", "name: pchange", "amount", "buy", "bratio", "sell", "sratio", "reason", "date"
# 代码 名称 当日涨跌幅 龙虎榜成交额(万) 买入额(万) 买入占总成交比例 卖出额(万) 卖出占总成交比例 上榜原因 日期


STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="每日数据",
        name="龙虎榜",
        table_name="ts_top_list",
        columns=["date", "code", "name", "pchange", "amount", "buy", "bratio", "sell", "sratio", "reason"],
        column_names=["日期", "代码", "名称", "当日涨跌幅", "龙虎榜成交额(万)", "买入额(万)", "买入占总成交比例", "卖出额(万)",
                      "卖出占总成交比例", "上榜原因"],
        primary_key=[],
        order_by=" date desc  "
    )
)

######################### 最后是editor 配置 #########################
STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="editor",
        type="股票配置管理",
        name="持仓管理",
        table_name="user_stock",
        columns=["code", "date", "price", "shares", "commission_rate", "tax_rate", "comment"],
        column_names=["股票代码", "日期", "价格", "数量", "佣金", "税率", "备注"],
        primary_key=["code", "date"],
        order_by=" code desc "
    )
)

STOCK_WEB_DATA_MAP = {}
# 再拼接成Map使用。
for tmp in STOCK_WEB_DATA_LIST:
    STOCK_WEB_DATA_MAP[tmp.table_name] = tmp
    if len(tmp.columns) != len(tmp.column_names):
        print(u"error:", tmp.table_name, ",columns:", len(tmp.columns), ",column_names:", len(tmp.column_names))
