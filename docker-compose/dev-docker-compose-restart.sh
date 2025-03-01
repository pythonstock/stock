#!/bin/sh


git pull

sleep 1
docker-compose -f dev-docker-compose.yml down

sleep 1
docker-compose -f dev-docker-compose.yml up -d

echo "restart dev-docker-compose"

