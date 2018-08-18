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

# 每日波峰波谷猜想
STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="每日数据猜想",
        name="每日波峰波谷猜想",
        table_name="guess_period_daily",
        columns=["date", "code", "name", "wave_base", "wave_crest", "wave_mean", "up_rate",
                 "changepercent", "trade", "open", "high", "low", "settlement", "volume",
                 "turnoverratio", "amount", "per", "pb", "mktcap", "nmc"],
        column_names=["日期", "代码", "名称", "5波峰平均", "5波谷平均", "价格平均", "上涨率猜想%",
                      "涨跌幅", "现价", "开盘价", "最高价", "最低价", "昨日收盘价", "成交量",
                      "换手率", "成交金额", "市盈率", "市净率", "总市值", "流通市值"],
        primary_key=[],
        order_by=" date desc  "
    )
)

# 每日收益率猜想。
STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="每日数据猜想",
        name="每日收益率猜想",
        table_name="guess_return_daily",
        columns=["date", "code", "name",
                 "5d", "10d", "20d", "60d", "5-10d", "5-20d", "mov_vol", "return",
                 "changepercent", "trade", "open", "high", "low", "settlement", "volume",
                 "turnoverratio", "amount", "per", "pb", "mktcap", "nmc"],
        column_names=["日期", "代码", "名称",
                      "5周线", "10半月线", "20月线", "60季度线", "5-10日差%", "5-20日差%", "收益", "收益率移动标准差",
                      "涨跌幅", "现价", "开盘价", "最高价", "最低价", "昨日收盘价", "成交量",
                      "换手率", "成交金额", "市盈率", "市净率", "总市值", "流通市值"],
        primary_key=[],
        order_by=" date desc  "
    )
)

# 每日股票指标lite猜想。
STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="每日数据猜想",
        name="每日股票指标lite猜想",
        table_name="guess_indicators_lite_daily",
        columns=["date", "code", "name", "changepercent", "trade", "open", "high", "low", "settlement", "volume",
                 "turnoverratio", "amount", "per", "pb", "mktcap", "nmc",
                 "kdjj", "rsi_6", "cci"],
        column_names=["日期", "代码", "名称",
                      "涨跌幅", "现价", "开盘价", "最高价", "最低价", "昨日收盘价", "成交量",
                      "换手率", "成交金额", "市盈率", "市净率", "总市值", "流通市值",
                      "kdjj", "rsi_6", "cci"],
        primary_key=[],
        order_by=" date desc  "
    )
)

# 每日股票指标lite猜想买入。
STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="每日数据猜想",
        name="每日股票指标lite猜想买入",
        table_name="guess_indicators_lite_buy_daily",
        columns=["buy_date", "code", "name", "changepercent", "trade", "turnoverratio", "pb",
                 "kdjj", "rsi_6", "cci", "wave_base", "wave_crest", "wave_mean", "up_rate", "buy", "sell",
                 "today_trade", "income"],
        column_names=["购买日期", "代码", "名称", "涨跌幅", "现价", "换手率%", "市净率%",
                      "买入kdjj", "买入rsi_6", "买入cci", "波谷", "波峰", "波平均", "上涨率%", "买入", "卖出", "今日价格", "收益"],
        primary_key=[],
        order_by=" buy_date desc  "
    )
)

# 每日股票指标lite猜想卖出。
STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="每日数据猜想",
        name="每日股票指标lite猜想卖出",
        table_name="guess_indicators_lite_sell_daily",
        columns=["date", "buy_date", "code", "name", "changepercent", "trade", "turnoverratio", "pb",
                 "kdjj", "rsi_6", "cci", "wave_base", "wave_crest", "wave_mean", "up_rate", "buy", "sell",
                 "today_trade", "income", "sell_cci", "sell_kdjj", "sell_rsi_6"],
        column_names=["日期", "购买日期", "代码", "名称", "涨跌幅", "现价", "换手率%", "市净率%",
                      "买入kdjj", "买入rsi_6", "买入cci", "波谷", "波峰", "波平均", "上涨率%", "买入", "卖出", "今日价格", "收益",
                      "卖出kdjj", "卖出rsi_6", "卖出cci", ],
        primary_key=[],
        order_by=" buy_date desc  "
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

STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="每日数据Keras猜想",
        name="每日股票数据Keras猜想",
        table_name="guess_sklearn_ma_daily",
        columns=["date", "code", "name", "changepercent", "trade", "open", "high", "low", "settlement", "volume",
                 "turnoverratio", "next_close", "sklearn_score", "up_rate"],
        column_names=["日期", "代码", "名称", "涨跌幅", "现价", "开盘价", "最高价", "最低价", "昨日收盘价", "成交量",
                      "换手率", "预测收盘价", "sk概率", "预测上涨率"],
        primary_key=[],
        order_by=" date desc  "
    )
)

STOCK_WEB_DATA_MAP = {}
WEB_EASTMONEY_URL = "http://quote.eastmoney.com/%s.html"
# 再拼接成Map使用。
for tmp in STOCK_WEB_DATA_LIST:
    try:
        # 增加columns 字段中的【东方财富】
        tmp_idx = tmp.columns.index("code")
        tmp.column_names.insert(tmp_idx + 1, "东方财富")
    except  Exception as e:
        print("error :", e)

    STOCK_WEB_DATA_MAP[tmp.table_name] = tmp

    if len(tmp.columns) != len(tmp.column_names):
        print(u"error:", tmp.table_name, ",columns:", len(tmp.columns), ",column_names:", len(tmp.column_names))
