#!/bin/sh

DOCKER_TAG=pythonstock/pythonstock:latest

sudo rm -rf data
sudo rm -f jobs/nohup.out

echo " docker build -f Dockerfile -t ${DOCKER_TAG} ."
docker build -f Dockerfile -t ${DOCKER_TAG} .
echo "#################################################################"
echo " docker push ${DOCKER_TAG} "

mkdir data

