<h1>notification-gateway-lite</h1>

# 简介

notification-gateway-lite 是一个非常轻量的通知网关，可以聚合各种推送渠道，使用 Serverless 部署，几乎零成本运行。

# 特性

- 支持各种常见的推送渠道，如Bark、企业微信等
- 支持部署成腾讯云Serverless，几乎零成本运行
- 解决因为群晖DSM奇怪的webhook设置方式而无法接入一些推送渠道的问题

## 目前支持的通知方式

- [Bark](https://github.com/Finb/Bark)
- [企业微信应用消息](https://developer.work.weixin.qq.com/document/path/90236)
- [企业微信机器人webhook](https://developer.work.weixin.qq.com/document/path/91770)
- [Pushover](https://pushover.net/api) [未测试]
- [PushDeer](http://pushdeer.com) [未测试]

### 可能会支持的推送方式
- [ ] 钉钉
- [ ] pushplus
- [ ] ...

> 如果有需要的通知方式，请提交issue


# 部署方式

- [腾讯云Serverless](docs/deploy/TencentcloudServerless.md)
- [阿里云Serverless](docs/deploy/AliyunServerless.md)
- [Docker](docs/deploy/Docker.md) （支持 `arm64`、`amd64`架构）

# 接口文档

见 [接口文档](docs/Api.md)

# 示例应用

- [使用 notification-gateway-lite 接收群晖DSM推送](docs/example/DSM.md)

# 微信交流群
![](http://img.ameow.xyz/202205291706791.jpg)
