#!/bin/sh


cd ..
DOCKER_TAG=github.com/pythonstock/stock/tensorflow-py3-stock:latest

echo "docker build -f DockerStock -t ${DOCKER_TAG} ."
docker build -f ./docker/DockerStock -t ${DOCKER_TAG} .