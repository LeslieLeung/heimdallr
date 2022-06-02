<h1>使用 Docker 部署 notification-gateway-lite </h1>

# 前提

本文章默认你已经理解并熟悉 Docker，并配置好 Docker 运行环境。

# 安装

需要通过 `-e` 配置对应的环境变量，详情见 [环境变量](/docs/Env.md) 。

> 自 `v0.1.1` 起 Docker 镜像支持 `arm64` 架构。

```bash
docker pull leslieleung/notification-gateway-lite:latest
docker run -d --name=notification-gateway-lite -p 9000:9000 -e ENV=VAL leslieleung/notification-gateway-lite:latest
```

# 更新

```bash
docker pull leslieleung/notification-gateway-lite:latest
docker stop notification-gateway-lite
docker rm notification-gateway-lite
docker run -d --name=notification-gateway-lite -p 9000:9000 -e ENV=VAL leslieleung/notification-gateway-lite:latest
```