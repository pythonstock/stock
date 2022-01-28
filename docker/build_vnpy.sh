#!/bin/sh


NOW_MONTH=$(date "+%Y-%m")

#DOCKER_TAG=gao9/vnpy:${NOW_MONTH}
DOCKER_TAG=gao9/vnpy:latest

echo " docker build -f Dockerfile -t ${DOCKER_TAG} ."
docker build -f Dockerfile_vnpy -t ${DOCKER_TAG} .
echo "#################################################################"
echo " docker push ${DOCKER_TAG} "


