<h1>接口文档</h1>

# Path Variable Style
`/{channel}/{title}/{body}`

- `channel` 为推送的渠道，可以是 `bark`、`wecom-webhook`、`wecom-app` 等。
- `title` 为推送的标题，可以是任意字符串。（可以不填）
- `body` 为推送的内容，可以是任意字符串。

# Get Param Style

`/{channel}?title={title}&body={body}`
- `channel` 为推送的渠道，可以是 `bark`、`wecom-webhook`、`wecom-app` 等。
- `title` 为推送的标题，可以是任意字符串。（可以不填）
- `body` 为推送的内容，可以是任意字符串。