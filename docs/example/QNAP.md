<h1>使用 Heimdallr 接收威联通推送</h1>

进入【通知中心】-【服务帐户和设备配对】-【短信】，点击【添加 SMSC 服务】。

SMS 服务提供商选择 【custom】，别名随意选择即可。【URL 模板】填入以下信息。剩余两项随意填写即可。

```
https://example.com/key?phone=@@PhoneNumber@@&title=Notification+From+QNAP&body=@@Text@@
```
`example.com` 替换为你的服务地址，`key` 为你的通知渠道的 `token`。


![](http://img.ameow.xyz/202311010122299.png)

点击创建后，即可看到刚才创建的通知方式。

![](http://img.ameow.xyz/202311010128631.png)

点击小飞机（发送测试消息），收到通知即为配置成功。

再来到【系统通知规则】，进入【警报通知】，选择创建规则，下一步，在收件人处选择【短信】方式，选择刚才添加的服务，手机号码随意填写即可。

![](http://img.ameow.xyz/202311010129263.png)