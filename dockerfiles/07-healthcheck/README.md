
# 练习 7：健康检查

**目标**：理解 `HEALTHCHECK` 指令以及它在容器编排中的作用。

**涉及**：`HEALTHCHECK`、`docker inspect` 中的健康状态

---

## Step 1：构建

    docker build -t health-demo 07-healthcheck/

## Step 2：运行并查看健康状态

    docker run -d -p 8007:8000 --name health-check health-demo

等待几秒，查看健康状态：

    docker inspect health-check --format '{{.State.Health.Status}}'

也可以用：

    docker ps
    # 在 STATUS 列能看到 (healthy)

## Step 3：理解 HEALTHCHECK 参数

    HEALTHCHECK --interval=5s --timeout=3s --retries=2 \
      CMD python -c "..." || exit 1

| 参数 | 含义 |
|------|------|
| `--interval` | 每多久检查一次 |
| `--timeout` | 单次检查超时 |
| `--retries` | 连续失败几次算不健康 |
| `--start-period` | 容器启动后多久才开始检查 |

## Step 4：模拟不健康

访问 `/slow` 端点，服务会卡 5 秒，可能触发健康检查超时：

    curl http://localhost:8007/slow &
    docker inspect health-check --format '{{json .State.Health}}' | python3 -m json.tool

## Step 5：清理

    docker rm -f health-check

## 检查清单

- [ ] 理解 `HEALTHCHECK` 的语法和参数含义
- [ ] 能用 `docker inspect` 查看健康状态
- [ ] 理解健康检查在编排中的作用

## 思考题

1. `HEALTHCHECK` 和 `docker run --restart` 有什么关系？能自动重启不健康容器吗？
2. Compose 文件中的 `healthcheck` 字段和 Dockerfile 中的 `HEALTHCHECK`，哪个优先级高？
3. 为什么要设计 `start-period`？哪些类型的应用特别需要它？

---

Phase 2 练习全部完成！可以进入 [Phase 3：Docker Compose](../compose/README.md)
