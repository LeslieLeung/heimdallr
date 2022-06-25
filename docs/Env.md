<h1>环境变量设置</h1>

## 目前支持的环境变量

本项目使用环境变量传入诸如企业微信机器人webhook key等token，防止重要信息泄露。
各种通知渠道的参数按需设置即可，不需要的渠道可以不设置。

> ***重要安全建议*** ：debug 模式打开时，会在控制台输出系统实际的请求和返回信息，可能会包含你的token等隐私信息，请注意仅在调试时启用该功能。

| 变量名                | 通知渠道      | 变量说明                                                                                                                  |
|--------------------|-----------|-----------------------------------------------------------------------------------------------------------------------|
| `KEY`              | Heimdallr | 用于本服务鉴权的key，使用 Docker 部署时建议填写。                                                                                        |
| `DEBUG`            | Heimdallr | 用于表示是否进入 debug 模式，设置该变量并填入任意值即可（例如 `1` ），会在日志中打印出请求和返回参数，方便调试。                                                        |
| `BARK_URL`         | Bark      | Bark服务器地址，如`https://api.day.app`                                                                                      |
| `BARK_KEY`         | Bark      | Bark的推送 key，如 `qy7s8qnhjhphuNDHJNFxQE`                                                                                |
| `WECOM_KEY`        | 企业微信      | 企业微信机器人的 key，见 [企业微信机器人webhook](https://developer.work.weixin.qq.com/document/path/91770)                             |
| `WECOM_CORP_ID`    | 企业微信      | 企业微信应用的 corp_id，见 [企业微信应用消息](https://developer.work.weixin.qq.com/document/path/90236)                                |
| `WECOM_AGENT_ID`   | 企业微信      | 企业微信应用的 agent_id                                                                                                      |
| `WECOM_SECRET`     | 企业微信      | 企业微信应用的 secret                                                                                                        |
| `PUSHOVER_TOKEN`   | Pushover  | Pushover 的 token，见 [Pushover API](https://pushover.net/api)                                                           |
| `PUSHOVER_USER`    | Pushover  | Pushover 的 user                                                                                                       |
| `PUSHDEER_TOKEN`   | PushDeer  | PushDeer 的 token，见 [Pushdeer API](http://pushdeer.com)                                                                |
| `CHANIFY_ENDPOINT` | Chanify   | Chanify 的 endpoint，见 [Chanify](https://github.com/chanify/chanify#as-sender-client)，可不填，默认为 `https://api.chanify.net` |
| `CHANIFY_TOKEN`    | Chanify   | Chanify 的 token                                                                                                       |


## 腾讯云 Serverless 环境变量设置

在创建函数时可以在高级配置中创建环境变量，函数创建后，可以在【函数配置-编辑】处对环境变量进一步进行设置。

![](http://img.ameow.xyz/202205290601686.png)

## Docker 环境变量设置

> 阿里云 Serverless、华为云 Serverless 的配置方法类似。

在使用 `docker run` 命令创建容器时，可以通过 `-e ENV=ENV_VAL` 的方式创建环境变量。