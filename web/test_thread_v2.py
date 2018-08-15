#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import time
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, asynchronous, RequestHandler
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

# `pip install futures` for python2

# https://gist.github.com/methane/2185380 参考

html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
      <script src="http://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js"></script>
</head>
<body>
    <h1>任务测试</h1></br>
    <button id="job">开始</button>
</body>
</html>
<script type="text/javascript">
    function job_check(timer,tid) {
        $.ajax({
           type: "GET",
           url: "job_check?tid="+tid,
           success: function(msg){
                console.log(msg);
                if(msg != ""){
                    alert( "任务结果: " + msg );
                    clearInterval(timer);//结束轮询
                }
            }
        });
    }
	jQuery(function($) {
	    
	    $("#job").click( function () {
	        $.ajax({
               type: "GET",
               url: "add_job",
               success: function(tid){
                    alert( "开始任务: " + tid );
                    timer = setInterval(function(){
                        console.log("run.");
                        job_check(timer,tid);
                    },1000);
               }
            });
	    });
	})
</script>
"""


class MainPage(RequestHandler):
    def get(self):
        self.write(html_content)


MAX_WORKERS = 4
_result = {}


class AddJobHandler(RequestHandler):
    # 必须定义一个executor的属性，然后run_on_executor 注解才管用。
    executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

    @run_on_executor  # 标记成后台程序执行。
    def background_task(self, tid):
        time.sleep(10)  # 传递参数 10 秒。
        _result[tid] = {"finish"}

    @gen.coroutine
    def get(self):
        tid = str(int(time.time() * 10000))
        self.background_task(tid)
        self.write(tid)


class JobCheckHandler(RequestHandler):
    def get(self):
        tid = self.get_argument("tid")
        if tid in _result.keys():
            out = _result[tid]  # 结果
            del _result[tid]  # 删除tid的数据。
            self.write(str(out))
        else:
            self.write("")


# main 启动。
if __name__ == "__main__":
    HTTPServer(Application([
        ("/", MainPage),
        ("/add_job", AddJobHandler),
        ("/job_check", JobCheckHandler)
    ], debug=True)).listen(9999)
    print("start web .")
    IOLoop.instance().start()
