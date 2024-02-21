<h1>使用 Heimdallr 接收 rsspush 推送</h1>

先按照 [rsspush](https://github.com/easychen/rsspush) 文档安装配置好 RSSPush。

在 SendKey 处，填入 Heimdallr 的 webhook，如下。

```
https://example.com/webhook/rsspush/{key}
```

其中 `{key}` 为通知渠道的 `token`。

> 提示：RSSPush 没有提供测试通知渠道的方式，如果需要测试，可以把拉取时间间隔调为1分钟，然后从 [Lorem RSS](https://lorem-rss.herokuapp.com/) 这个网站复制 `https://lorem-rss.herokuapp.com/feed` 到 RSS 订阅处，即可每隔一分钟触发一次。

## 加餐 —— 接收 V2EX 新消息
在 V2EX [提醒系统](https://v2ex.com/notifications) 底部有一个【Atom Feed for Notifications】，复制该地址到 RSSPush 中即可接收 V2EX 新消息推送。