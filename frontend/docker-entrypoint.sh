#!/bin/sh

sleep 1
# 只依赖启动。
cd /usr/src/app

#!/bin/bash

# 定义要检查的文件夹路径
modules_path="/usr/src/app/node_modules"

# 使用[ ]检查文件夹是否存在
if [ -d "$modules_path" ]; then
    echo "文件夹 $modules_path 存在"
else
    echo "文件夹 $modules_path 不存在，执行 install 安装"
    npm install --registry=https://registry.npmmirror.com
fi

npm run dev
sleep 999999d
