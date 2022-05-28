<h1>环境变量设置</h1>

## 目前支持的环境变量

本项目使用环境变量传入诸如企业微信机器人webhook key等token，防止重要信息泄露。
各种通知渠道的参数按需设置即可，不需要的渠道可以不设置。

| 变量名              | 通知渠道 | 变量说明                                                                                     |
|------------------|------|------------------------------------------------------------------------------------------|
| `BARK_URL`       | Bark | Bark服务器地址，如`https://api.day.app`                                                         |
| `BARK_KEY`       | Bark | Bark的推送key，如 `qy7s8qnhjhphuNDHJNFxQE`                                                    |
| `WECOM_KEY`      | 企业微信 | 企业微信机器人的key，见 [企业微信机器人webhook](https://developer.work.weixin.qq.com/document/path/91770) |
| `WECOM_CORP_ID`  | 企业微信 | 企业微信应用的corp_id，见 [企业微信应用消息](https://developer.work.weixin.qq.com/document/path/90236)    |
| `WECOM_AGENT_ID` | 企业微信 | 企业微信应用的agent_id                                                                          |
| `WECOM_SECRET`   | 企业微信 | 企业微信应用的secret                                                                            |

## 腾讯云 Serverless 环境变量设置

在创建函数时可以在高级配置中创建环境变量，函数创建后，可以在【函数配置-编辑】处对环境变量进一步进行设置。

![](http://img.ameow.xyz/202205290601686.png)