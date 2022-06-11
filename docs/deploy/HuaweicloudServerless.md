<h1>使用华为云 Serverless 部署</h1>

> 由于华为云与其他云的 Serverless 略有不同，该部分教程正在完善，未能投入实用。

# 前提

本文章默认你已经理解并熟悉 git 和 Docker，并安装好相应的软件。

# Step 1. 配置华为云镜像仓库

进入华为云 [容器镜像服务](https://console.huaweicloud.com/swr)，左上角需要选择合适的地域（镜像仓库所在的地域要与函数的地域一致）。

点击右上角【创建组织】，输入组织名称，点击确定新建组织。

参考文章 [获取长期有效登录指令](https://support.huaweicloud.com/usermanual-swr/swr_01_1000.html) 获取长期登录secret。

> ### Tips
> 在获取到 `AK` 和 `SK` 后，可以使用以下命令获取登录密钥。
> ```bash
> export AK=xxx
> export SK=xxx
> printf "$AK" | openssl dgst -binary -sha256 -hmac "$SK" | od -An -vtx1 | sed 's/[ \n]//g' | sed 'N;s/\n//'
> ```

使用登录指令登录镜像仓库。

```bash
docker login -u [区域项目名称]@[AK] -p [登录密钥] [镜像仓库地址]
```

# Step 2. 构建镜像并推送至仓库

先克隆本项目至本地。

```bash
git clone https://github.com/LeslieLeung/notification-gateway-lite.git
cd notification-gateway-lite
```

记住之前创建的组织名称和镜像仓库地址，这里给镜像打 tag 需要用到。这里将 `YOUR_NAMESPACE` 替换成命名空间的名字，`YOUR_REPOSITORY` 替换成仓库的名字。`VERSION` 可以随便取，但建议使用递增的数字。

```bash
docker build -t [镜像仓库地址]/YOUR_NAMESPACE/YOUR_REPO_NAME:VERSION .
docker push [镜像仓库地址]/YOUR_NAMESPACE/YOUR_REPO_NAME:VERSION
```

在【我的镜像】中应该能查看到构建的镜像。

![](http://img.ameow.xyz/202206112024600.png)

# Step 3. 创建 Serverless 函数

进入华为云 [函数工作流](https://console.huaweicloud.com/functiongraph) ，选择【创建函数】。

选择容器镜像，函数类型选择HTTP函数，函数名称随意选择，容器镜像输入刚才swr开头的那个（如`swr.cn-south-1.myhuaweicloud.com/ameow/notification-gateway-lite:v0.0.31`）。

点击【容器镜像覆盖】，展开菜单，在【Args】处配置环境变量（详见 [环境变量](../Env.md)）。

最下面，如果没有现有委托，请选择创建委托。【云服务】处搜索选择【函数工作流】。

![](http://img.ameow.xyz/202206112036205.png)

右上角输入 `SWR` 搜索，勾选 `SWR Admin` 。

![](http://img.ameow.xyz/202206112031810.png)

输入 `function` 搜索，勾选 `FunctionGraph Administrator`, 点击下一步，然后确认即可。

![](http://img.ameow.xyz/202206112034200.png)

回到云函数页面，选择刚才创建的委托，点击创建函数，稍等即创建完成。

点击设置-触发器，创建一个触发器。如没有分组，创建一个，发布环境选择默认的【RELEASE】即可。安全认证选择【None】，点击确认即可。

![](http://img.ameow.xyz/202206112042273.png)

创建好后，即可看到 api 地址。

> ！重要提示 此访问路径为访问推送服务的唯一鉴权途径，请妥善保存避免泄露。

![](http://img.ameow.xyz/202206112043997.png)

# 大功告成！

至此，基于华为云 Serverless 的部署已经完成。使用方式详见 [接口文档](../Api.md)。