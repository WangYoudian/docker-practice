
# 练习 1：Web + Redis

**目标**：用 Compose 定义两个服务，理解服务间的网络联通和 Compose 的基本语法。

**涉及**：`services`、`build`、`image`、`ports`、`environment`、`volumes`

---

## Step 1：查看 compose.yml

    cat 01-web-redis/compose.yml

定义了两个服务：
- `app`：从 `./app` 构建 Python 应用
- `redis`：直接使用官方 `redis:7-alpine` 镜像

## Step 2：启动

    cd 01-web-redis
    docker compose up -d

首次启动会构建 app 镜像、拉取 redis 镜像、创建网络和 volume。

## Step 3：验证

    curl http://localhost:8101
    # 输出: Visit count: 1

    curl http://localhost:8101
    # 输出: Visit count: 2

每次请求计数器 +1，数据存在 Redis 中。

## Step 4：检查 Compose 创建的资源

    docker compose ps          # 查看服务状态
    docker compose logs        # 查看日志
    docker compose images      # 查看使用的镜像
    docker network ls          # 可以看到 compose 自动创建的网络
    docker volume ls           # 可以看到 compose 创建的 volume

## Step 5：理解网络

Compose 自动创建一个默认网络，所有服务可以通过**服务名称**互相访问。
`app` 里用 `REDIS_HOST=redis` 连接到了 `redis` 服务，不需要知道 IP。

## 清理

    docker compose down -v     # 停止服务并删除 volume
    cd ..

## 检查清单

- [ ] 理解 `compose.yml` 的基本结构（services / volumes / networks）
- [ ] 能使用 `docker compose up -d` 启动
- [ ] 理解 Compose 中的服务发现（通过服务名通信）
- [ ] 知道 `docker compose ps / logs / down` 等管理命令

## 思考题

1. 如果不指定 `ports`，app 服务能从宿主机访问到吗？
2. `docker compose up -d` 和 `docker compose up -d --build` 有什么区别？
3. Redis 的 `volumes: - redis-data:/data` 是 named volume 还是 bind mount？数据还存在吗？
4. 如果我想让 app 和 redis 使用独立的网络，不在同一个默认网络里，怎么写？
