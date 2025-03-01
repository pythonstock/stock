## 镜像仓库选择

https://github.com/DaoCloud/public-image-mirror

```bash

# python使用镜像
docker.m.daocloud.io/library/python:3.11-slim-bullseye

# mysql使用：
docker.m.daocloud.io/library/mysql:8

```


## 本地部署方法


```
git clone git@gitee.com:pythonstock/docker-compose.git

cd docker-compose

docker-compose up -d

```

## 访问地址

http://localhost:9090/



## 查看日至，进入项目代码

```
# 查看启动日志：
docker logs -f stock

# 进入stock容器
docker exec -it stock bash
```

## 开发模式，映射stock 代码方法

直接使用 dev yml 即可，会映射stock到/data/stock 然后在外部修改代码容器中运行即可。

```bash
docker-compose  -f dev-docker-compose.yml  up -d
```

```bash
docker-compose  -f docker-compose-v2.0.yml up -d
```

## 老镜像还保存一个版本

```
pythonstock/pythonstock:v2021
```