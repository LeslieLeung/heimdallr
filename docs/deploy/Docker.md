<h1>使用 Docker 部署 Heimdallr </h1>

# 前提

本文章默认你已经理解并熟悉 Docker，并配置好 Docker 运行环境。

# 安装

需要通过 `-e` 配置对应的环境变量，详情见 [环境变量](/docs/Env.md) 。

> 自 `v0.1.1` 起 Docker 镜像支持 `arm64` 架构。

```bash
docker pull leslieleung/heimdallr:latest
docker run -d --name=heimdallr -p 9000:9000 -e ENV=VAL leslieleung/heimdallr:latest
```

# 更新

> 最后一条 `run` 命令需要保持与第一次创建时一致，可以使用 `history | grep heimdallr` 查询。

如果需要更新环境变量，请在 `run` 命令中更新。

```bash
docker pull leslieleung/heimdallr:latest
docker stop heimdallr
docker rm heimdallr
docker run -d --name=heimdallr -p 9000:9000 -e ENV=VAL leslieleung/heimdallr:latest
```