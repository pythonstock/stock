#!/bin/sh

ps -ef | grep 'tensorflow_model_server' | grep -v grep | awk '{print$2}' | xargs kill -9
echo "" > /data/logs/mnist_serving.log
nohup tensorflow_model_server --model_name=mnist --model_base_path=/data/mnist_model >> /data/logs/mnist_serving.log &