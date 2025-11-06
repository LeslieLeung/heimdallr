# 使用 Docker 部署 Heimdallr V3

## 前提

本文章默认你已经理解并熟悉 Docker 和 Docker Compose，并配置好 Docker 运行环境。

## V3 架构说明

Heimdallr V3 采用前后端分离架构：

- **Backend**: FastAPI + Python，提供 RESTful API 服务
- **Frontend**: React + TypeScript，提供 Web UI 界面
- **Database**: 支持 SQLite（默认）或 MySQL

## 部署方式

Heimdallr V3 提供三种部署方式：

### 方式一：使用 Docker Compose（推荐）

这是最简单快速的部署方式，适合生产环境。

#### 1. 下载部署文件

```bash
# 下载 docker-compose.yml 和 .env.example
curl -O https://raw.githubusercontent.com/LeslieLeung/heimdallr/v3-dev/docker-compose.yml
curl -O https://raw.githubusercontent.com/LeslieLeung/heimdallr/v3-dev/.env.example

# 复制并编辑环境变量文件
cp .env.example .env
```

#### 2. 配置环境变量

编辑 `.env` 文件，至少需要修改以下配置：

```bash
# 必须修改：生产环境密钥
SECRET_KEY=your_random_secret_key_here

# 可选：域名配置
DOMAIN=your-domain.com

# 可选：端口配置
BACKEND_PORT=9000
FRONTEND_PORT=80
```

#### 3. 启动服务

```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

#### 4. 访问服务

- 前端界面: `http://localhost` (或配置的端口)
- 后端 API: `http://localhost:9000` (或配置的端口)
- API 文档: `http://localhost:9000/docs`

### 方式二：分别运行前后端容器

如果你想更灵活地控制各个组件，可以分别运行容器。

#### 1. 运行后端

```bash
docker run -d \
  --name heimdallr-backend \
  -p 9000:9000 \
  -e DATABASE_DSN=sqlite:////app/data/heimdallr.db \
  -e SECRET_KEY=your_random_secret_key_here \
  -e DOMAIN=localhost \
  -v ./data/heimdallr:/app/data \
  leslieleung/heimdallr-backend:latest
```

#### 2. 运行前端

```bash
docker run -d \
  --name heimdallr-frontend \
  -p 80:80 \
  --link heimdallr-backend:backend \
  leslieleung/heimdallr-frontend:latest
```

### 方式三：从源码构建（开发环境）

适合需要修改代码或开发新功能的场景。

#### 1. 克隆仓库

```bash
git clone -b v3-dev https://github.com/LeslieLeung/heimdallr.git
cd heimdallr
```

#### 2. 使用开发环境 Compose

```bash
# 启动开发环境（包含热重载）
cd deploy
docker-compose -f dev.docker-compose.yaml up -d

# 查看日志
docker-compose -f dev.docker-compose.yaml logs -f
```

开发环境特点：
- 代码热重载：修改代码后自动重启
- 包含 MySQL 数据库
- 调试模式开启
- 前端开发服务器运行在 5173 端口

## 数据库配置

### 使用 SQLite（默认）

默认使用 SQLite，适合单机部署，无需额外配置。

```bash
DATABASE_DSN=sqlite:////app/data/heimdallr.db
```

数据文件位置：`./data/heimdallr/heimdallr.db`

### 使用 MySQL

适合需要高可用或多实例部署的场景。

#### 1. 在 docker-compose.yml 中启用 MySQL

取消注释 MySQL 服务配置部分。

#### 2. 配置环境变量

```bash
# MySQL 配置
MYSQL_ROOT_PASSWORD=secure_root_password
MYSQL_DATABASE=heimdallr
MYSQL_USER=heimdallr
MYSQL_PASSWORD=secure_password

# 后端连接配置
DATABASE_DSN=mysql+pymysql://heimdallr:secure_password@mysql:3306/heimdallr
```

#### 3. 启动服务

```bash
docker-compose --profile mysql up -d
```

## 镜像说明

### 镜像版本标签

- `latest`: 最新稳定版本（跟随 main 分支）
- `v3-dev`: V3 开发版本
- `v3.x.x`: 特定版本号
- `v3-dev-{sha}`: 基于特定 commit 构建

### 支持的架构

所有镜像支持以下架构：
- `linux/amd64` (x86_64)
- `linux/arm64` (ARM64/AArch64)

自 `v0.1.1` 起支持 ARM64 架构，可在树莓派、ARM 服务器等设备上运行。

### 镜像列表

- **后端镜像**: `leslieleung/heimdallr-backend`
- **前端镜像**: `leslieleung/heimdallr-frontend`

## 更新

### 使用 Docker Compose

```bash
# 拉取最新镜像
docker-compose pull

# 停止并删除旧容器
docker-compose down

# 启动新容器
docker-compose up -d
```

### 手动更新

```bash
# 拉取最新镜像
docker pull leslieleung/heimdallr-backend:latest
docker pull leslieleung/heimdallr-frontend:latest

# 停止并删除旧容器
docker stop heimdallr-backend heimdallr-frontend
docker rm heimdallr-backend heimdallr-frontend

# 启动新容器（使用与创建时相同的命令）
# 可以使用 history | grep heimdallr 查询历史命令
docker run -d --name=heimdallr-backend ...
docker run -d --name=heimdallr-frontend ...
```

## 配置说明

### 环境变量

完整的环境变量列表请参考 [配置文档](/docs/Config.md)。

主要配置项：

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `SECRET_KEY` | JWT 密钥（生产环境必须修改） | - |
| `DATABASE_DSN` | 数据库连接字符串 | `sqlite:////app/data/heimdallr.db` |
| `DEBUG` | 调试模式 | `false` |
| `WORKERS` | uvicorn 工作进程数 | `2` |
| `DOMAIN` | 域名 | `localhost` |
| `BACKEND_PORT` | 后端端口 | `9000` |
| `FRONTEND_PORT` | 前端端口 | `80` |

### 数据持久化

确保以下目录被正确挂载以持久化数据：

```yaml
volumes:
  # SQLite 数据库
  - ./data/heimdallr:/app/data

  # MySQL 数据（如果使用）
  - ./data/mysql:/var/lib/mysql

  # SSL 证书（如果使用 HTTPS）
  - ./data/ssl:/etc/nginx/ssl
```

## 健康检查

### 后端健康检查

```bash
curl http://localhost:9000/health
```

返回示例：
```json
{
  "status": "healthy",
  "version": "3.0.0",
  "commit": "abc1234"
}
```

### 前端健康检查

```bash
curl -I http://localhost
```

应返回 `200 OK` 状态码。

## 安全建议

1. **修改默认密钥**: 生产环境必须修改 `SECRET_KEY`
2. **使用 HTTPS**: 生产环境建议配置 SSL 证书
3. **限制端口暴露**: 生产环境建议只暴露前端端口，后端通过反向代理访问
4. **定期更新**: 及时更新到最新版本以获取安全修复
5. **备份数据**: 定期备份数据库文件

## 反向代理配置

### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端
    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 后端 API
    location /api/ {
        proxy_pass http://localhost:9000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Traefik 配置示例

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.heimdallr.rule=Host(`your-domain.com`)"
  - "traefik.http.services.heimdallr.loadbalancer.server.port=80"
```

## 故障排除

### 无法连接到后端

1. 检查后端容器是否运行：`docker ps | grep backend`
2. 查看后端日志：`docker logs heimdallr-backend`
3. 检查网络连接：`docker network inspect heimdallr-network`

### 数据库连接失败

1. 检查 `DATABASE_DSN` 配置是否正确
2. 如果使用 MySQL，确保 MySQL 容器已启动并健康
3. 检查数据库用户权限

### 前端页面空白

1. 检查浏览器控制台错误
2. 确认后端 API 地址配置正确
3. 检查 CORS 配置

### 权限问题

```bash
# 修复 SQLite 数据目录权限
sudo chown -R 1000:1000 ./data/heimdallr

# 修复 MySQL 数据目录权限（如果使用）
sudo chown -R 999:999 ./data/mysql
```

## 监控和日志

### 查看日志

```bash
# 所有服务日志
docker-compose logs -f

# 仅后端日志
docker-compose logs -f backend

# 仅前端日志
docker-compose logs -f frontend

# 最近 100 行日志
docker-compose logs --tail=100
```

### 资源监控

```bash
# 查看容器资源使用情况
docker stats heimdallr-backend heimdallr-frontend
```

## 性能优化

### 增加工作进程

对于高并发场景，可以增加后端工作进程数：

```bash
WORKERS=4
```

推荐配置：`CPU 核心数 * 2 + 1`

### 使用外部缓存

对于大规模部署，建议使用 Redis 等缓存服务。

## 备份和恢复

### 备份 SQLite 数据库

```bash
# 停止服务
docker-compose stop backend

# 备份数据库
cp ./data/heimdallr/heimdallr.db ./backup/heimdallr-$(date +%Y%m%d).db

# 启动服务
docker-compose start backend
```

### 备份 MySQL 数据库

```bash
docker exec heimdallr-mysql mysqldump -u heimdallr -p heimdallr > backup-$(date +%Y%m%d).sql
```

### 恢复数据库

```bash
# SQLite
docker-compose stop backend
cp ./backup/heimdallr-20240101.db ./data/heimdallr/heimdallr.db
docker-compose start backend

# MySQL
docker exec -i heimdallr-mysql mysql -u heimdallr -p heimdallr < backup-20240101.sql
```

## 常见问题

### Q: V3 和 V2 有什么区别？

A: V3 采用前后端分离架构，提供更好的用户体验和可扩展性。主要改进：
- 现代化的 Web UI
- RESTful API 设计
- 更好的性能和可维护性
- 支持更多部署方式

### Q: 如何从 V2 迁移到 V3？

A: 目前需要重新配置，V2 数据不能直接迁移到 V3。建议：
1. 导出 V2 配置
2. 部署 V3
3. 在 V3 中重新配置

### Q: 支持 Docker Swarm 或 Kubernetes 吗？

A: 镜像完全支持容器编排，参考 docker-compose.yml 配置即可部署到 Swarm 或 K8s。

### Q: 如何配置 HTTPS？

A: 建议使用 Nginx 或 Traefik 等反向代理配置 SSL，或参考 `deploy/docker-compose.prod.yaml` 中的配置。

## 更多文档

- [配置文档](/docs/Config.md)
- [API 文档](/docs/Api.md)
- [快速开始](/docs/QUICK_START.md)
- [GitHub 仓库](https://github.com/LeslieLeung/heimdallr)

## 获取帮助

如有问题，欢迎：
- 提交 [GitHub Issue](https://github.com/LeslieLeung/heimdallr/issues)
- 查看 [讨论区](https://github.com/LeslieLeung/heimdallr/discussions)
