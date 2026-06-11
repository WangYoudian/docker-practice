
# 练习 3：依赖与健康检查

**目标**：理解 `depends_on` 的三种模式，掌握等待依赖服务就绪的正确方式。

**涉及**：`depends_on`、`condition: service_healthy`、多文件 Compose

---

## 背景

简单的 `depends_on` 只能控制**启动顺序**，不能保证服务**已经就绪**。
PostgreSQL 启动后还需要几秒才能接受连接，如果 app 在这段时间内连接就会报错。

## Step 1：查看基础版本

    cat 03-dependencies/compose.yml

这里用了简单的 `depends_on: - db`，只能保证 db 容器先启动，但不保证它已就绪。

## Step 2：查看带健康检查的版本

    cat 03-dependencies/compose.health.yml

关键变化：
- db 服务加了 `healthcheck` 定义
- app 的 `depends_on` 加了 `condition: service_healthy`

这样 app 会等待 db 的健康检查通过后才启动。

## Step 3：启动带健康检查的版本

    cd 03-dependencies
    docker compose -f compose.yml -f compose.health.yml up -d

加上 `-f compose.health.yml` 后，Compose 会把两个文件合并（override 文件追加 healthcheck 配置）。

## Step 4：观察启动顺序

    docker compose logs -f

可以看到 db 先启动，然后反复执行 `pg_isready` 直到就绪，之后 app 才开始启动。

## Step 5：验证

    curl http://localhost:8103

## 清理

    docker compose down -v
    cd ..

## 关于多种依赖模式

| 模式 | 含义 |
|------|------|
| `depends_on: - db` | 启动顺序，不等就绪 |
| `condition: service_started` | 等同于简单版，不常用 |
| `condition: service_healthy` | 必须等待健康检查通过 |
| `condition: service_completed_successfully` | 等待另一个服务成功退出 |

## 检查清单

- [ ] 理解 `depends_on` 和健康检查的区别
- [ ] 能写带 `condition: service_healthy` 的 Compose 配置
- [ ] 理解多文件 Compose (`-f`) 的合并机制

## 思考题

1. 如果不做健康检查，app 在 db 未就绪时连接数据库会怎样？什么机制可以重试？
2. `condition: service_completed_successfully` 适合什么场景？（提示：迁移任务、初始化任务）
3. docker compose 的 `--wait` 参数和健康检查有什么关联？
4. Compose 的 depends_on 和 Kubernetes 的 initContainer 是什么关系？
