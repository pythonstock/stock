#!/bin/sh

DOCKER_TAG=pythonstock/pythonstock:latest

echo "docker build -f Dockerfile -t ${DOCKER_TAG} ."
docker build -f Dockerfile -t ${DOCKER_TAG} .
#docker push ${DOCKER_TAG}