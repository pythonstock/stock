#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import time
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, asynchronous, RequestHandler
from multiprocessing.pool import ThreadPool
from multiprocessing.pool import ApplyResult
from tornado import gen

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


_workers = ThreadPool(10)
_result = {}


# 后台任务。
def blocking_task(n, tid):
    time.sleep(n)
    print(tid)
    _result[tid] = {"finish"}


class AddJobHandler(RequestHandler):
    @gen.coroutine
    def get(self):
        tid = str(int(time.time() * 10000))
        _workers.apply_async(blocking_task, (10, tid))  # 传递参数 10 秒。
        self.write(tid)
        self.finish()  # 先finish 掉，然后在后台执行。


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
