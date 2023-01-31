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


# https://www.akshare.xyz/zh_CN/latest/data/stock/stock.html#id1
# 限量: 单次返回所有 A 股上市公司的实时行情数据
STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="1，股票基本数据",
        name="每日股票数据-东财",
        table_name="stock_zh_ah_name",
        columns=['date','code','name','latest_price','quote_change','ups_downs','volume','turnover',
                 'amplitude','high','low','open','closed','quantity_ratio','turnover_rate','pe_dynamic','pb'],
        column_names=['日期','代码','名称','最新价','涨跌幅','涨跌额','成交量','成交额',
                      '振幅','最高','最低','今开','昨收','量比','换手率','动态市盈率','市净率'],
        primary_key=[],
        order_by=" code asc "
    )
)

STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="1，股票基本数据",
        name="龙虎榜-个股上榜-新浪",
        table_name="stock_sina_lhb_ggtj",
        columns= ['date','code','name','ranking_times','sum_buy','sum_sell','net_amount','buy_seat','sell_seat'],
        column_names=['日期','代码', '名称', '上榜次数', '累积购买额', '累积卖出额', '净额', '买入席位数', '卖出席位数'],
        primary_key=[],
        order_by=" code asc "
    )
)

STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="1，股票基本数据",
        name="数据中心-大宗交易",
        table_name="stock_dzjy_mrtj",
        columns= ['date', 'code', 'name', 'quote_change', 'close_price', 'average_price',
                                   'overflow_rate', 'trade_number', 'sum_volume', 'sum_turnover',
                                   'turnover_market_rate'],
        column_names=['日期', '代码', '名称', '涨跌幅', '收盘价', '成交均价',
                      '折溢率', '成交笔数', '成交总量', '成交总额',
                      '成交总额/流通市值'],
        primary_key=[],
        order_by=" code asc "
    )
)



# 每日股票指标lite猜想买入。
STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="2，每日数据猜想",
        name="股票指标lite猜想买入",
        table_name="guess_indicators_lite_buy_daily",
        columns=['date', 'code', 'name', 'latest_price', 'quote_change', 'ups_downs', 'volume', 'turnover',
                 'amplitude', 'high', 'low', 'open', 'closed', 'quantity_ratio', 'turnover_rate', 'pe_dynamic', 'pb',
                 'kdjj', 'rsi_6', 'cci'],
        column_names=['日期', '代码', '名称', '最新价', '涨跌幅', '涨跌额', '成交量', '成交额',
                      '振幅', '最高', '最低', '今开', '昨收', '量比', '换手率', '动态市盈率', '市净率',
                      'kdjj', 'rsi_6', 'cci'],
        primary_key=[],
        order_by=" buy_date desc  "
    )
)

# 每日股票指标lite猜想卖出。
STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="2，每日数据猜想",
        name="股票指标lite猜想卖出",
        table_name="guess_indicators_lite_sell_daily",
        columns=['date', 'code', 'name', 'latest_price', 'quote_change', 'ups_downs', 'volume', 'turnover',
                 'amplitude', 'high', 'low', 'open', 'closed', 'quantity_ratio', 'turnover_rate', 'pe_dynamic', 'pb',
                 'kdjj', 'rsi_6', 'cci'],
        column_names=['日期', '代码', '名称', '最新价', '涨跌幅', '涨跌额', '成交量', '成交额',
                      '振幅', '最高', '最低', '今开', '昨收', '量比', '换手率', '动态市盈率', '市净率',
                      'kdjj', 'rsi_6', 'cci'],
        primary_key=[],
        order_by=" buy_date desc  "
    )
)

# 每日股票指标lite猜想。
STOCK_WEB_DATA_LIST.append(
    StockWebData(
        mode="query",
        type="2，每日数据猜想",
        name="股票指标猜想原始数据",
        table_name="guess_indicators_daily",
        columns=['date','code','name','latest_price','quote_change','ups_downs',
                 'adx', 'adxr', 'boll', 'boll_lb', 'boll_ub', 'cci', 'cci_20', 'close_-1_r',
                    'close_-2_r', 'code', 'cr', 'cr-ma1', 'cr-ma2', 'cr-ma3', 'date', 'dma', 'dx',
                    'kdjd', 'kdjj', 'kdjk', 'macd', 'macdh', 'macds', 'mdi', 'pdi',
                    'rsi_12', 'rsi_6', 'trix', 'trix_9_sma', 'vr', 'vr_6_sma', 'wr_10', 'wr_6'],
        column_names=['日期','代码','名称','最新价','涨跌幅','涨跌额',
                      'adx', 'adxr', 'boll', 'boll_lb', 'boll_ub', 'cci', 'cci_20', 'close_-1_r',
                    'close_-2_r', 'code', 'cr', 'cr-ma1', 'cr-ma2', 'cr-ma3', 'date', 'dma', 'dx',
                    'kdjd', 'kdjj', 'kdjk', 'macd', 'macdh', 'macds', 'mdi', 'pdi',
                    'rsi_12', 'rsi_6', 'trix', 'trix_9_sma', 'vr', 'vr_6_sma', 'wr_10', 'wr_6'],
        primary_key=[],
        order_by=' date desc  '
    )
)

# "code", "name: pchange", "amount", "buy", "bratio", "sell", "sratio", "reason", "date"
# 代码 名称 当日涨跌幅 龙虎榜成交额(万) 买入额(万) 买入占总成交比例 卖出额(万) 卖出占总成交比例 上榜原因 日期


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
