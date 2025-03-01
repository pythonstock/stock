#!/bin/sh

cd ../stock

NOW_MONTH=$(date "+%Y-%m")

DOCKER_TAG=pythonstock/pythonstock:latest
DOCKER_TAG_MONTH=pythonstock/pythonstock:stock-${NOW_MONTH}

echo " docker build -f Dockerfile -t ${DOCKER_TAG} ."
docker build -f Dockerfile -t ${DOCKER_TAG} .
echo " docker build tag xxx ${DOCKER_TAG_MONTH} "
echo "#################################################################"
echo " docker push ${DOCKER_TAG} "


