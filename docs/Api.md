<h1>接口文档</h1>

# Path Variable Style
`/{channel}/{title}/{body}/{key}`

- `channel` 为推送的渠道，可以是 `bark`、`wecom-webhook`、`wecom-app` 等。
- `title` 为推送的标题，可以是任意字符串。（可以不填）
- `body` 为推送的内容，可以是任意字符串。
- `key` 为环境变量中设置的key，当设置了环境变量时必填。

# Get Param Style

`/{channel}?title={title}&body={body}&key={key}`
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