<h1>接口文档</h1>

> 接口文档有 [在线版](https://service-epwdrzxg-1255787947.gz.apigw.tencentcs.com/release/docs) ，本文档更新可能较在线版晚。

# 通用

## channel 取值

目前支持以下通知渠道

- `bark` - [Bark](https://github.com/Finb/Bark)
- `wecom-app` - [企业微信应用消息](https://developer.work.weixin.qq.com/document/path/90236)
- `wecom-webhook` - [企业微信机器人webhook](https://developer.work.weixin.qq.com/document/path/91770)
- `pushover` - [Pushover](https://pushover.net/api)
- `pushdeer` - [PushDeer](http://pushdeer.com)

### <div id="multi-channel">推送到多个渠道</div>

> `v0.1.3` 后支持推送到多个渠道

需要推送到多个渠道时，`channel` 参数传入多个渠道，以 `+` 分隔，如 `bark+wecom-app+wecom-webhook` 。

# 接口

## Path Variable Style
`/{channel}/{title}/{body}/{key}`

>  `GET` / `POST`

- `channel` 为推送的渠道，可以是 `bark`、`wecom-webhook`、`wecom-app` 等。
- `title` 为推送的标题，可以是任意字符串。（可以不填）
- `body` 为推送的内容，可以是任意字符串。
- `key` 为环境变量中设置的key，当设置了环境变量时必填。

## Get Param Style

`/{channel}?title={title}&body={body}&key={key}`

> `GET`

- `channel` 为推送的渠道，可以是 `bark`、`wecom-webhook`、`wecom-app` 等。
- `title` 为推送的标题，可以是任意字符串。（可以不填）
- `body` 为推送的内容，可以是任意字符串。
- `key` 为环境变量中设置的key，当设置了环境变量时必填。

## JSON

`/send`

> `POST`

请求参数

```json
{
  "channel": "string",
  "title": "",
  "body": "",
  "key": ""
}
```

## Form

`/sendForm`

> `POST`

- `channel` 为推送的渠道，可以是 `bark`、`wecom-webhook`、`wecom-app` 等。
- `title` 为推送的标题，可以是任意字符串。（可以不填）
- `body` 为推送的内容，可以是任意字符串。
- `key` 为环境变量中设置的key，当设置了环境变量时必填。

# 返回示例

## 成功
```json
{"code": 0, "message": "success"}
```

## 错误

### 通知渠道返回错误信息

```json
{"code": 1, "message": "{channel} return {msg}"}
```

### 不支持的渠道

```json
{"code": 2, "message": "{channel} is not supported"}
```

### 运行错误

```json
{"code": 3, "message": "xxx"}
```

### 认证错误

```json
{"code": -1, "message": "key not authorized"}
```