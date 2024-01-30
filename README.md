<h1>Heimdallr</h1>

> 🔧该项目已经重构至新版本，API、配置项 等与原v1.x版本不兼容。若需要用旧版，请查看 [legacy 分支](https://github.com/LeslieLeung/heimdallr/tree/legacy) 。

# 简介

Heimdallr 是一个非常轻量的通知网关，可以聚合各种推送渠道，使用 Serverless 部署，几乎零成本运行。

# 特性

- 等同于免费、开源、可自建的 [新版Server酱](https://sct.ftqq.com/)，没有任何限制，痛快推送
- 支持各种常见的推送渠道，如Bark、企业微信等
- 完全兼容 Bark 的路由，任意支持 Bark 的地方，都可以使用 Heimdallr 同时发送到更多渠道
- 支持多通知渠道和分组配置
- 支持 Serverless 部署，几乎零成本运行
- 解决因为群晖DSM奇怪的 webhook 设置方式而无法接入一些推送渠道的问题

## 目前支持的通知方式

- [Bark](https://github.com/Finb/Bark)
- [企业微信应用消息](https://developer.work.weixin.qq.com/document/path/90236)
- [企业微信机器人webhook](https://developer.work.weixin.qq.com/document/path/91770)
- [PushDeer](http://pushdeer.com)
- [Chanify](https://github.com/chanify/chanify) [未测试]
- [Pushover](https://pushover.net/api) [未测试]
- Email
- [Discord(webhook)](https://discord.com/developers/docs/resources/webhook#execute-webhook)
- [Telegram Bot](https://core.telegram.org/bots/api#sendmessage)
- [ntfy](https://docs.ntfy.sh/)
- [飞书/Lark](https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot)


### 可能会支持的推送方式
- [ ] 钉钉
- [ ] ...

> 如果有需要的通知方式，请提交 [issue](https://github.com/LeslieLeung/heimdallr/issues/new?assignees=LeslieLeung&labels=enhancement&template=feature_request.md&title=)


# 部署方式

配置项见 [示例](.env.example)。

具体配置，见 [配置文档](docs/Config.md)

## 第三方服务

### Zeabur

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/E7FFAQ?referralCode=LeslieLeung)

> 配置方式参考 [文档](https://zeabur.com/docs/zh-CN/environment/variables)，在编辑原始环境变量处粘贴 `.env` 的内容即可。

## Serverless
- [腾讯云Serverless](docs/deploy/TencentcloudServerless.md)
- [阿里云Serverless](docs/deploy/AliyunServerless.md)

## Docker
见 [Docker](docs/deploy/Docker.md) （支持 `arm64`、`amd64`架构）

# 接口文档

见 [接口文档](https://heimdallr.zeabur.app/docs) 。

## Markdown 支持

在一些支持 Markdown 的服务上，格式化的文本可以以 Markdown 格式呈现。在请求时，通过 query 参数或 json 传入 `msg_type = markdown` 即可。

示例：

```bash
# GET
curl 'http://<HOST>/<TOKEN>/*Hello*/__World__?msg_type=markdown'
# POST
curl -X POST 'http://<HOST>/push' --data-raw '{
    "key": "<TOKEN>",
    "title": "*Hello*",
    "body": "__World__",
    "msg_type": "markdown"
}'
```

> 注意，支持 Markdown 的服务中，并非所有服务都采用相同的语法。在不支持 Markdown 的服务，内容将以纯文本展示。
>
> 当前支持 Markdown 的服务及其支持的语法如下：
> - [企业微信](https://developer.work.weixin.qq.com/document/path/90236#%E6%94%AF%E6%8C%81%E7%9A%84markdown%E8%AF%AD%E6%B3%95)
> - [Discord](https://support.discord.com/hc/en-us/articles/210298617-Markdown-Text-101-Chat-Formatting-Bold-Italic-Underline)
> - [Telegram](https://core.telegram.org/bots/api#markdownv2-style)

# 示例应用

- [使用 Heimdallr 接收群晖DSM推送](docs/example/DSM.md)
- [使用 Heimdallr 接收威联通推送](docs/example/QNAP.md)
- [使用 Heimdallr 接收 GitHub star webhook](docs/example/GitHubStar.md)

# 更新日志

见 [更新日志](docs/Changelog.md)