#!/bin/sh


DOCKER_TAG=github.com/pythonstock/stock/tensorflow-serving:latest

echo "docker build -f DockerServing -t ${DOCKER_TAG} ."
docker build -f ./DockerServing -t ${DOCKER_TAG} .

docker run -itd --name tf-serving  \
    -v ~/PyWorkspace/stock-github:/data/stock \
    -p 8500:8500 \
   github.com/pythonstock/stock/tensorflow-serving:latest
