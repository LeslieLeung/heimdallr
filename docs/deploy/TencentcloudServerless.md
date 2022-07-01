<h1>使用腾讯云 Serverless 部署</h1>

# 前提

本文章默认你已经理解并熟悉 git 和 Docker，并安装好相应的软件。

# 安装

## Step 1. 配置腾讯云镜像仓库

由于腾讯云 Serverless 的限制，使用容器镜像来创建函数时，必须从自己的容器镜像服务选择镜像，所以必须自行构建 docker 镜像。

首先需要新建一个 [命名空间](https://console.cloud.tencent.com/tcr/namespace) ，第一次使用腾讯云容器镜像服务时，可能需要点击开通个人版，该功能不需要收费，放心开通即可。

同时此处可能会提示给镜像服务设置一个密码，这个密码仅供镜像仓库使用且与腾讯云账号独立（可以认为是一个 docker 镜像私服的账号密码）。

命名空间的名字可以随便取。然后进入 [镜像仓库](https://console.cloud.tencent.com/tcr/repository)，点击新建一个仓库，名称可以取 `heimdallr`，类型选择私有，命名空间选择刚才新建的，然后点击确认即可。

新仓库创建好后，点击快捷指令，复制登录的命令，在命令行中运行，根据提示输入刚才设置的镜像仓库密码，登录到镜像仓库。

![](http://img.ameow.xyz/202205290540180.png)


## Step 2. 构建镜像并推送至仓库[buildImage]

先克隆本项目至本地。

```bash
git clone https://github.com/LeslieLeung/heimdallr.git
cd heimdallr
```

记住之前创建的命名空间和仓库的名称，这里给镜像打 tag 需要用到。这里将 `YOUR_NAMESPACE` 替换成命名空间的名字，`YOUR_REPOSITORY` 替换成仓库的名字。`VERSION` 可以随便取，但建议使用递增的数字。

```bash
docker build -t ccr.ccs.tencentyun.com/YOUR_NAMESPACE/YOUR_REPO_NAME:VERSION .
docker push ccr.ccs.tencentyun.com/YOUR_NAMESPACE/YOUR_REPO_NAME:VERSION
```

回到镜像仓库，应该可以看到里面已经有刚才构建好的镜像。

![](http://img.ameow.xyz/202205290548858.png)


## Step 3. 创建 Serverless 函数

进入 [腾讯云 Serverless](https://console.cloud.tencent.com/scf/list) ，选择新建。（此处如果是第一次使用 Serverless，可能会需要开通一些东西，跟随页面提示操作即可）。

在新建页面，选择【使用容器镜像】，函数类型选择【Web函数】，函数名称随便填，地域按需选择。

![](http://img.ameow.xyz/202205290551452.png)

函数代码处，点击选择镜像，选择刚才的镜像仓库，选择刚才推送的镜像，点击提交。

![](http://img.ameow.xyz/202205290552175.png)

点击展开高级配置，内存选择【64MB】，然后根据 [环境变量配置](../Env.md) 进行配置。

![](http://img.ameow.xyz/202205290554815.png)

其他设置保持默认，拉到最下面点击完成即可。

创建完成后，来到函数管理-函数代码处，可以看到访问路径。

> ！重要提示 此访问路径为访问推送服务的唯一鉴权途径，请妥善保存避免泄露。

![](http://img.ameow.xyz/202205290556488.png)

## 大功告成！

至此，基于腾讯云 Serverless 的部署已经完成。使用方式详见 [接口文档](../Api.md)。

# 升级

## Step 1. 构建新版镜像

此处与首次安装时 [构建](#step-2-buildimage) 方法一致，注意版本号建议不要使用与之前相同的。

```bash
cd heimdallr
git pull
docker build -t ccr.ccs.tencentyun.com/YOUR_NAMESPACE/YOUR_REPO_NAME:VERSION .
docker push ccr.ccs.tencentyun.com/YOUR_NAMESPACE/YOUR_REPO_NAME:VERSION
```

## Step 2. 部署新版镜像

在函数服务中，进入对应函数的管理页面，点击【函数管理】-【函数代码】-【镜像配置】-【编辑】。

点击【选择镜像】，选择仓库和镜像版本，点击提交，点击保存，待部署完成后即更新成功。

## Step 3. （可选）更新环境变量

新版本镜像可能支持了更多通知渠道，因此需要对应新增环境变量。在【函数配置】页面，点击编辑，新增环境变量后拉到最下面点击保存即可。