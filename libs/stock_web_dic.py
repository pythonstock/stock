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

STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="基本面数据",
        name="沪深300成份股",
        table_name="ts_stock_hs300s",
        columns=["code", "name", "weight"],
        column_names=["代码", "名称", "权重"],
        primary_key=[],
        order_by=" code asc "
    )
)

STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="基本面数据",
        name="中证500成份股",
        table_name="ts_stock_zz500s",
        columns=["code", "name", "weight"],
        column_names=["代码", "名称", "权重"],
        primary_key=[],
        order_by=" code asc "
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
# 实时行情
STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="每日数据",
        name="每日股票数据",
        table_name="ts_today_all",
        columns=["date", "code", "name", "changepercent", "trade", "open", "high", "low", "settlement", "volume",
                 "turnoverratio", "amount", "per", "pb", "mktcap", "nmc"],
        column_names=["日期", "代码", "名称", "涨跌幅", "现价", "开盘价", "最高价", "最低价", "昨日收盘价", "成交量",
                      "换手率", "成交金额", "市盈率", "市净率", "总市值", "流通市值"],
        primary_key=[],
        order_by=" date desc  "
    )
)
# 大盘指数行情列表
STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="每日数据",
        name="每日大盘指数行情",
        table_name="ts_index_all",
        columns=["date", "code", "name", "change", "open", "preclose", "close", "high", "low", "volume", "amount"],
        column_names=["日期", "代码", "名称", "涨跌幅", "开盘点位", "昨日收盘点位", "收盘点位", "最高点位", "最低点位", "成交量(手)", "成交金额（亿元）"],
        primary_key=[],
        order_by=" date desc  "
    )
)


# 每日股票指标猜想。
STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="每日数据猜想",
        name="每日股票指标All猜想",
        table_name="guess_indicators_daily",
        columns=["date", "code", "name", "changepercent", "trade", "open", "high", "low", "settlement", "volume",
                 "turnoverratio", "amount", "per", "pb", "mktcap", "nmc",
                 'adx', 'adxr', 'boll', 'boll_lb', 'boll_ub', 'cci', 'cci_20', 'close_-1_r',
                 'close_-2_r', 'code', 'cr', 'cr-ma1', 'cr-ma2', 'cr-ma3', 'date', 'dma', 'dx',
                 'kdjd', 'kdjj', 'kdjk', 'macd', 'macdh', 'macds', 'mdi', 'pdi',
                 'rsi_12', 'rsi_6', 'trix', 'trix_9_sma', 'vr', 'vr_6_sma', 'wr_10', 'wr_6'],
        column_names=["日期", "代码", "名称",
                      "涨跌幅", "现价", "开盘价", "最高价", "最低价", "昨日收盘价", "成交量",
                      "换手率", "成交金额", "市盈率", "市净率", "总市值", "流通市值",
                      'adx', 'adxr', 'boll', 'boll_lb', 'boll_ub', 'cci', 'cci_20', 'close_-1_r',
                      'close_-2_r', 'code', 'cr', 'cr-ma1', 'cr-ma2', 'cr-ma3', 'date', 'dma', 'dx',
                      'kdjd', 'kdjj', 'kdjk', 'macd', 'macdh', 'macds', 'mdi', 'pdi',
                      'rsi_12', 'rsi_6', 'trix', 'trix_9_sma', 'vr', 'vr_6_sma', 'wr_10', 'wr_6'],
        primary_key=[],
        order_by=" date desc  "
    )
)
# 每日股票指标lite猜想买入。
STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="每日数据猜想",
        name="每日股票指标买入猜想",
        table_name="guess_indicators_lite_buy_daily",
        columns=["date", "code", "name", "changepercent", "trade", "open", "high", "low", "settlement", "volume",
                 "turnoverratio", "amount", "per", "pb", "mktcap", "nmc",
                 "kdjj", "rsi_6", "cci"],
        column_names=["日期", "代码", "名称",
                      "涨跌幅", "现价", "开盘价", "最高价", "最低价", "昨日收盘价", "成交量",
                      "换手率", "成交金额", "市盈率", "市净率", "总市值", "流通市值",
                      "kdjj", "rsi_6", "cci"],
        primary_key=[],
        order_by=" buy_date desc  "
    )
)

# 每日股票指标lite猜想卖出。
STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="每日数据猜想",
        name="每日股票指标卖出猜想",
        table_name="guess_indicators_lite_sell_daily",
        columns=["date", "code", "name", "changepercent", "trade", "open", "high", "low", "settlement", "volume",
                 "turnoverratio", "amount", "per", "pb", "mktcap", "nmc",
                 "kdjj", "rsi_6", "cci"],
        column_names=["日期", "代码", "名称",
                      "涨跌幅", "现价", "开盘价", "最高价", "最低价", "昨日收盘价", "成交量",
                      "换手率", "成交金额", "市盈率", "市净率", "总市值", "流通市值",
                      "kdjj", "rsi_6", "cci"],
        primary_key=[],
        order_by=" buy_date desc  "
    )
)

STOCK_WEB_DATA_MAP = {}
WEB_EASTMONEY_URL = "http://quote.eastmoney.com/%s.html"
# 再拼接成Map使用。
for tmp in STOCK_WEB_DATA_LIST:
    try:
        # 增加columns 字段中的【查看股票】
        tmp_idx = tmp.columns.index("code")
        tmp.column_names.insert(tmp_idx + 1, "查看股票")
    except  Exception as e:
        print("error :", e)

    STOCK_WEB_DATA_MAP[tmp.table_name] = tmp

    if len(tmp.columns) != len(tmp.column_names):
        print(u"error:", tmp.table_name, ",columns:", len(tmp.columns), ",column_names:", len(tmp.column_names))
