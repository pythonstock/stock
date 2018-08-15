#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


from tornado import gen
# import sys
# import os
# sys.path.append(os.path.abspath('/data/stock/libs'))
import libs.stock_web_dic as stock_web_dic
import web.base as webBase
import logging
import re

# 获得页面数据。
class GetEditorHtmlHandler(webBase.BaseHandler):
    @gen.coroutine
    def get(self):
        name = self.get_argument("table_name", default=None, strip=False)
        stockWeb = stock_web_dic.STOCK_WEB_DATA_MAP[name]
        # self.uri_ = ("self.request.url:", self.request.uri)
        # print self.uri_
        self.render("data_editor.html", stockWeb=stockWeb, leftMenu=webBase.GetLeftMenu(self.request.uri))


# 拼接sql，将value的key 和 value 放到一起。
def genSql(primary_key, param_map, join_string):
    tmp_sql = ""
    idx = 0
    for tmp_key in primary_key:
        tmp_val = param_map[tmp_key]
        if idx == 0:
            tmp_sql = " `%s` = '%s' " % (tmp_key, tmp_val)
        else:
            tmp_sql += join_string + (" `%s` = '%s' " % (tmp_key, tmp_val))
        idx += 1
    return tmp_sql


# 获得页面数据。
class SaveEditorHandler(webBase.BaseHandler):
    @gen.coroutine
    def post(self):
        action = self.get_argument("action", default=None, strip=False)
        logging.info(action)
        table_name = self.get_argument("table_name", default=None, strip=False)
        stockWeb = stock_web_dic.STOCK_WEB_DATA_MAP[table_name]
        # 临时map数组。
        param_map = {}
        # 支持多排序。使用shift+鼠标左键。
        for item, val in self.request.arguments.items():
            # 正则查找  data[1112][code] 里面的code字段
            item_key = re.search(r"\]\[(.*?)\]", item)
            if item_key:
                tmp_1 = item_key.group()
                if tmp_1:
                    tmp_1 = tmp_1.replace("][", "").replace("]", "")
                    param_map[tmp_1] = val[0].decode("utf-8")
        #logging.info(param_map)
        if action == "create":
            logging.info("###########################create")
            # 拼接where 和 update 语句。
            tmp_columns = "`, `".join(stockWeb.columns)
            tmp_values = []
            for tmp_key in stockWeb.columns:
                tmp_values.append(param_map[tmp_key])
            # 更新sql。
            tmp_values2 = "', '".join(tmp_values)
            insert_sql = " INSERT INTO %s (`%s`) VALUES('%s'); " % (stockWeb.table_name, tmp_columns, tmp_values2)
            logging.info(insert_sql)
            try:
                self.db.execute(insert_sql)
            except Exception as e:
                err = {"error": str(e)}
                logging.info(err)
                self.write(err)
                return

        elif action == "edit":
            logging.info("###########################edit")
            # 拼接where 和 update 语句。
            tmp_update = genSql(stockWeb.columns, param_map, ",")
            tmp_where = genSql(stockWeb.primary_key, param_map, "and")
            # 更新sql。
            update_sql = " UPDATE %s SET %s WHERE %s " % (stockWeb.table_name, tmp_update, tmp_where)
            logging.info(update_sql)
            try:
                self.db.execute(update_sql)
            except Exception as e:
                err = {"error": str(e)}
                logging.info(err)
                self.write(err)
                return
        elif action == "remove":
            logging.info("###########################remove")
            # 拼接where 语句。
            tmp_where = genSql(stockWeb.primary_key, param_map, "and")
            # 更新sql。
            delete_sql = " DELETE FROM %s WHERE %s " % (stockWeb.table_name, tmp_where)
            logging.info(delete_sql)
            try:
                self.db.execute(delete_sql)
            except Exception as e:
                err = {"error": str(e)}
                logging.info(err)
                self.write(err)
                return
        self.write("{\"data\":[{}]}")
