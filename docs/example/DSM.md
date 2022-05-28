<h1>使用 notification-gateway-lite 接收群晖DSM推送</h1>

进入【控制面板】-【通知设置】-【短信】，点击【新增短信服务提供商】。

名称随意选择即可，测试网址填入在腾讯云 Serverless中获取的url，【测试网址】按照如下复制即可。如果使用 bark ，第一个地方填bark，若使用其他，填其他方式，具体见 [接口文档](/docs/Api.md) 。

```
https://SERVERLESS_URL/bark?phone=123&title=hi&body=hello+world
```

![](http://img.ameow.xyz/202205290618022.png)

点击下一步，在【编辑HTTP请求标题】页面留空，点下一步即可。

![](http://img.ameow.xyz/202205290621042.png)

在该页按照截图设置即可。最后点击应用。

![](http://img.ameow.xyz/202205290622353.png)

回到控制面板，选择刚才添加的短信服务提供商，发件人随便填，作为通知title，主要电话号码也是随便填即可。

![](http://img.ameow.xyz/202205290623132.png)

点击应用，然后点击【寄送测试短信】，若能收到通知，即配置成功。