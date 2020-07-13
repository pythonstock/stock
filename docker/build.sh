#!/bin/sh


NOW_MONTH=$(date "+%Y-%m")

DOCKER_TAG=pythonstock/pythonstock:base-${NOW_MONTH}

echo " docker build -f Dockerfile -t ${DOCKER_TAG} ."
docker build -f Dockerfile -t ${DOCKER_TAG} .
echo "#################################################################"
echo " docker push ${DOCKER_TAG} "


