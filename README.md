<h1>Heimdallr</h1>

> 🔧该项目目前正在重构，部署方式、API 等均不稳定，随时可能改变。若要使用稳定版本，请查看 [legacy 分支](https://github.com/LeslieLeung/heimdallr/tree/legacy) 。

# 简介

Heimdallr 是一个非常轻量的通知网关，可以聚合各种推送渠道，使用 Serverless 部署，几乎零成本运行。

# 特性

- 等同于免费、开源、可自建的 [新版Server酱](https://sct.ftqq.com/)，没有任何限制，痛快推送
- 支持各种常见的推送渠道，如Bark、企业微信等
- 支持部署成腾讯云Serverless，几乎零成本运行
- 解决因为群晖DSM奇怪的webhook设置方式而无法接入一些推送渠道的问题

## 目前支持的通知方式

- [Bark](https://github.com/Finb/Bark)
- [企业微信应用消息](https://developer.work.weixin.qq.com/document/path/90236)
- [企业微信机器人webhook](https://developer.work.weixin.qq.com/document/path/91770)
- [PushDeer](http://pushdeer.com)
- [Chanify](https://github.com/chanify/chanify)
- [Pushover](https://pushover.net/api) [未测试]
- Chanify
- Email

### 可能会支持的推送方式
- [ ] 钉钉
- [ ] Discord
- [ ] Telegram
- [ ] ...

> 如果有需要的通知方式，请提交 [issue](https://github.com/LeslieLeung/heimdallr/issues/new?assignees=LeslieLeung&labels=enhancement&template=feature_request.md&title=)


# 部署方式

## Serverless
- [腾讯云Serverless](docs/deploy/TencentcloudServerless.md)
- [阿里云Serverless](docs/deploy/AliyunServerless.md)

## Docker
见 [Docker](docs/deploy/Docker.md) （支持 `arm64`、`amd64`架构）

## 第三方服务

### Zeabur

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/E7FFAQ?referralCode=LeslieLeung)

# 接口文档

见 [在线版接口文档](https://service-epwdrzxg-1255787947.gz.apigw.tencentcs.com/release/docs) 或 [接口文档](docs/Api.md)

# 示例应用

- [使用 Heimdallr 接收群晖DSM推送](docs/example/DSM.md)
- [使用 Heimdallr 接收威联通推送](docs/example/QNAP.md)
- [使用 Heimdallr 接收 GitHub star webhook](docs/example/GitHubStar.md)

# 更新日志

见 [更新日志](docs/Changelog.md)