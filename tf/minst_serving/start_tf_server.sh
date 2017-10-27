#!/bin/sh


#判断文件夹存在不。
if [ ! -d "/data/mnist_model" ]; then
    mkdir -p /data/mnist_model
    python mnist_saved_model.py --training_iteration=5000 --model_version=1 /data/mnist_model
fi

ps -ef | grep tensorflow_model_server | awk '{print$2}' | xargs kill -9

tensorflow_model_server --model_name=mnist  --model_base_path=/data/mnist_model

echo "start tf server "