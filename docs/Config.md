<h1>配置指南</h1>

## 概述

本项目使用环境变量传入配置，防止重要信息泄露。

完整示例可参见 [示例](../.env.example)。

## 全局设置

> ***重要安全建议*** ：debug 模式打开时，会在控制台输出系统实际的请求和返回信息，可能会包含你的token等隐私信息，请注意仅在调试时启用该功能。

| 变量名    | 默认值  | 可选值          | 变量说明                                                                                    |
| --------- | ------- | --------------- | ------------------------------------------------------------------------------------------- |
| `DEBUG`   | `False` | `True`, `False` | 用于表示是否进入 debug 模式，会在日志中打印出请求和返回参数，方便调试。                     |
| `PORT`    | `9000`  |                 | 监听的端口号                                                                                |
| `WORKERS` | `1`     |                 | 服务线程数（增加服务线程可能会增加内存消耗，在 Serverless 部署时建议保持默认1个线程即可。） |

## 通知分组和渠道配置

本服务有分组和通知渠道的概念。通知渠道是最小的通知单位，可以通过某一个应用及其凭据发送通知；分组为多个通知渠道的组合，可以通过一个 `token` 唯一确定一个通知分组，同时向分组内的多个通知渠道发送通知。

见以下最小例子，其定义了一个名为 `group_1` 的分组，并具有一个对应的 `token`，启用了 `channel_1`, `channel_2`, `channel_3` 三个通知渠道。其中 `channel_1` 为 `bark` 类型，有 `BARK_URL` 和 `BARK_KEY` 两项配置；`channel_2`, `channel_3` 均为企业微信 Webhook。

```
ENABLED_GROUPS=group_1

# Define groups
# group_1
group_1_ENABLED_CHANNELS=channel_1,channel_2,channel_3
group_1_TOKEN=<YOUR_TOKEN>

# Define channels
# channel_1(bark)
channel_1_TYPE=bark
channel_1_BARK_URL=<YOUR_BARK_URL>
channel_1_BARK_KEY=<YOUR_BARK_KEY>

# channel_2(wecom_webhook)
channel_2_TYPE=wecom_webhook
channel_2_WECOM_WEBHOOK_KEY=<YOUR_WECOM_WEBHOOK_KEY>

# channel_3(wecom_app)
channel_3_TYPE=wecom_webhook
channel_3_WECOM_WEBHOOK_KEY=<YOUR_WECOM_WEBHOOK_KEY>
```

### 通知分组

| 变量名                        | 说明                                                                                      |
| ----------------------------- | ----------------------------------------------------------------------------------------- |
| ENABLED_GROUPS                | （必填）启用的分组，区分大小写，多个分组逗号隔开                                          |
| <GROUP_NAME>_ENABLED_CHANNELS | （必填）分组使用的通知渠道，区分大小写，多个渠道逗号隔开                                  |
| <GROUP_NAME>_TOKEN            | （必填）分组的 Token，对应请求时使用的 {key} 。建议使用随机生成的字母和数字，不可以带 `/` |

### 通知渠道

| 变量名              | 说明                                             |
| ------------------- | ------------------------------------------------ |
| <CHANNEL_NAME>_TYPE | （必填）渠道类型，取值范围见下表                 |
| (其他渠道配置)      | 渠道具体配置，形如 <CHANNEL_NAME>_<渠道配置后缀> |

#### 通知渠道类型

| 渠道名称         | 渠道类型（上面的`<CHANNEL_NAME>_TYPE` |
| ---------------- | ------------------------------------- |
| Bark             | bark                                  |
| 企业微信 Webhook | wecom_webhook                         |
| 企业微信应用     | wecom_app                             |
| Pushover         | pushover                              |
| PushDeer         | pushdeer                              |
| Chanify          | chanify                               |
| SMTP（邮件）     | email                                 |
| Discord          | discord_webhook                       |
| Telegram         | telegram                              |


#### 渠道配置后缀
| 后缀名                  | 通知渠道 | 后缀说明                                                                                                                                                                             |
| ----------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `BARK_URL`              | Bark     | Bark服务器地址，如`https://api.day.app`                                                                                                                                              |
| `BARK_KEY`              | Bark     | Bark的推送 key，如 `qy7s8qnhjhphuNDHJNFxQE`                                                                                                                                          |
| `WECOM_KEY`             | 企业微信 | 企业微信机器人的 key，见 [企业微信机器人webhook](https://developer.work.weixin.qq.com/document/path/91770)                                                                           |
| `WECOM_CORP_ID`         | 企业微信 | 企业微信应用的 corp_id，见 [企业微信应用消息](https://developer.work.weixin.qq.com/document/path/90236)                                                                              |
| `WECOM_AGENT_ID`        | 企业微信 | 企业微信应用的 agent_id                                                                                                                                                              |
| `WECOM_SECRET`          | 企业微信 | 企业微信应用的 secret                                                                                                                                                                |
| `PUSHOVER_TOKEN`        | Pushover | Pushover 的 token，见 [Pushover API](https://pushover.net/api)                                                                                                                       |
| `PUSHOVER_USER`         | Pushover | Pushover 的 user                                                                                                                                                                     |
| `PUSHDEER_TOKEN`        | PushDeer | PushDeer 的 token，见 [Pushdeer API](http://pushdeer.com)                                                                                                                            |
| `CHANIFY_ENDPOINT`      | Chanify  | Chanify 的 endpoint，见 [Chanify](https://github.com/chanify/chanify#as-sender-client)，可不填，默认为 `https://api.chanify.net`                                                     |
| `CHANIFY_TOKEN`         | Chanify  | Chanify 的 token                                                                                                                                                                     |
| `EMAIL_HOST`            | Email    | Email 服务器地址，如 `smtp.gmail.com`                                                                                                                                                |
| `EMAIL_PORT`            | Email    | Email 服务器端口，如 `465`                                                                                                                                                           |
| `EMAIL_USER`            | Email    | Email 用户名                                                                                                                                                                         |
| `EMAIL_PASSWORD`        | Email    | Email 密码                                                                                                                                                                           |
| `EMAIL_SENDER`          | Email    | Email 发件人名称                                                                                                                                                                     |
| `EMAIL_TO`              | Email    | Email 收件人                                                                                                                                                                         |
| `EMAIL_STARTTLS`        | Email    | Email 是否使用 TLS                                                                                                                                                                   |
| `DISCORD_WEBHOOK_ID`    | Discord  | Discord 的 Webhook ID，见 [Discord 文档](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)                                                                  |
| `DISCORD_WEBHOOK_TOKEN` | Discord  | Discord 的 Webhook Token                                                                                                                                                             |
| `TELEGRAM_TOKEN`        | Telegram | Telegram 的 Token，见 [这里](https://github.com/pppscn/SmsForwarder/wiki/2.%E5%8F%91%E9%80%81%E9%80%9A%E9%81%93#tele%E6%9C%BA%E5%99%A8%E4%BA%BA%E7%A7%91%E5%AD%A6%E4%B8%8A%E7%BD%91) |
| `TELEGRAM_CHAT_ID`      | Telegram | Telegram 的 Chat ID，见 [这里](https://github.com/pppscn/SmsForwarder/issues/319)                                                                                                    |


## 腾讯云 Serverless 环境变量设置

在创建函数时可以在高级配置中创建环境变量，函数创建后，可以在【函数配置-编辑】处对环境变量进一步进行设置。

![](http://img.ameow.xyz/202205290601686.png)

## Docker 环境变量设置

> 阿里云 Serverless、华为云 Serverless 的配置方法类似。

在使用 `docker run` 命令创建容器时，可以通过 `-e ENV=ENV_VAL` 的方式创建环境变量。

## Zeabur 环境变量配置

配置方式参考 [文档](https://zeabur.com/docs/zh-CN/environment/variables)，在编辑原始环境变量处粘贴 `.env` 的内容即可。

> 注意，Zeabur 的 `PORT` 变量固定为 `8080` ，不可调整。****
