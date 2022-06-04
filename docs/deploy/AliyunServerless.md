<h1>使用阿里云 Serverless 部署</h1>

# 前提

本文章默认你已经理解并熟悉 git 和 Docker，并安装好相应的软件。

# Step 1. 配置阿里云镜像仓库

进入阿里云 [容器镜像服务](https://cr.console.aliyun.com/)，左上角需要选择合适的地域（镜像仓库所在的地域要与函数的地域一致）。

![](http://img.ameow.xyz/202205291518320.png)

点击新建个人版实例。一路同意、确认即可，然后创建 Registry 密码。再点击创建镜像仓库，点击创建命名空间。

![](http://img.ameow.xyz/202205291521090.png)

填入仓库名称和摘要，选择私有，点下一步。

![](http://img.ameow.xyz/202205291522386.png)

然后选择【本地仓库】，点【创建镜像仓库】】。

![](http://img.ameow.xyz/202205291523191.png)

复制指南中的登录命令，如

```bash
docker login --username=是你猫兄啊 registry.cn-shenzhen.aliyuncs.com
```

输入密码登录。

# Step 2. 构建镜像并推送至仓库

先克隆本项目至本地。

```bash
git clone https://github.com/LeslieLeung/notification-gateway-lite.git
cd notification-gateway-lite
```

记住之前创建的命名空间和仓库的名称，这里给镜像打 tag 需要用到。这里将 `YOUR_NAMESPACE` 替换成命名空间的名字，`YOUR_REPOSITORY` 替换成仓库的名字。`VERSION` 可以随便取，但建议使用递增的数字。

```bash
docker build -t ccr.ccs.tencentyun.com/YOUR_NAMESPACE/YOUR_REPO_NAME:VERSION .
docker push ccr.ccs.tencentyun.com/YOUR_NAMESPACE/YOUR_REPO_NAME:VERSION
```

回到镜像仓库，在镜像版本中应该可以看到里面已经有刚才构建好的镜像。

![](http://img.ameow.xyz/202205291557281.png)

# Step 3. 创建 Serverless 函数

进入 [函数计算](https://fcnext.console.aliyun.com/)，注意地域需要选择和前面镜像仓库相同的地域。点击创建服务，名称随意填写，点击确定。

进入服务后，点击【函数管理】，点击【创建函数】。

选择【使用容器镜像创建】，函数名称随意输入，选择镜像，选择刚才构建的镜像。

![](http://img.ameow.xyz/202205291600858.png)

在 `Args` 处添加环境变量，如：

```bash
["-e", "BARK_URL=https://api.day.app"]
```

详细的环境变量列表，见 [环境变量](../Env.md) 。

如有多个环境变量请逐一添加。选择程序类型为【处理 HTTP 请求】，内存选择【128 MB】，点击创建即可。

![](http://img.ameow.xyz/202205291606498.png)

创建完成后，来到【函数管理-函数详情-触发器管理】处，可以看到访问路径。

> ！重要提示 此访问路径为访问推送服务的唯一鉴权途径，请妥善保存避免泄露。

![](http://img.ameow.xyz/202205291610517.png)

# 大功告成！

至此，基于阿里云 Serverless 的部署已经完成。使用方式详见 [接口文档](../Api.md)。