# 更新日志
## v2.0.4
- 支持 [rsspush](https://github.com/easychen/rsspush) webhook 通知。
## v2.0.3
- 通知渠道新增钉钉
## v2.0.2
- 通知渠道新增 飞书/Lark Webhook
## v2.0.1
- 通知渠道新增 ntfy
- 新增 `/push/form` 接口，支持 form-data
## v2.0.0-rc4
- 全面支持 Markdown
## v2.0.0-rc3
- 修复企业微信闲置长时间后 token 过期
## v2.0.0-rc2
- 增加支持 Telegram Bot
## v2.0.0-rc
大规模重构
- 完全兼容 Bark 的路由
- 支持多通知渠道和分组配置
## v1.2.4
- 增加 [威联通使用教程](docs/example/QNAP.md)
## v1.2.2
- 支持接收 GitHub star webhook，提醒获得新的 star [教程](docs/example/GitHubStar.md)
## v1.2.1
- 支持企业微信通知传入 Markdown 格式的文本。
## v1.2.0
- 新增一个 echo api，会把 POST 进来的内容原样返回。（预告：将来会用于接入 webhook。）
## v1.1.0
- 支持通过 json 传入配置，详见 [环境变量](docs/Env.md/#json)
## v1.0.1
- 支持 Email 通知
## v1.0.0
- 项目正式更名为 Heimdallr，其为北欧神话中彩虹桥的守护神，当诸神黄昏到来，海姆达尔将吹响号角，以便提醒众神
- 支持 Chanify 通知
## v0.1.5
- 修复 PushDeer 支持
## v0.1.4
- 新增 debug 模式，详见 [环境变量](docs/Env.md) 
## v0.1.3
- 支持同时推送到多个渠道，见 [接口文档](docs/Api.md/#multi-channel)
## v0.1.2
- 支持 `POST` 等更多接口，详见 [接口文档](docs/Api.md)
- 新增 [在线版接口文档](https://service-epwdrzxg-1255787947.gz.apigw.tencentcs.com/release/docs)