<h1>接口文档</h1>

接口文档见[这里](https://heimdallr.zeabur.app/docs)。

## 返回示例

### 成功
```json
{"code": 0, "message": "success"}
```

### 错误

#### 通知渠道返回错误信息

```json
{"code": 1, "message": "{channel} return {msg}"}
```

#### 认证错误

```json
{"code": -1, "message": "key is invalid"}
```