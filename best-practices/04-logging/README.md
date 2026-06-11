
# 练习 4：日志策略

**目标**：理解 Docker 日志体系，学会配置日志驱动和轮转策略。

**涉及**：`docker logs`、日志驱动、`max-size`、`max-file`

---

## 背景

Docker 默认把容器 stdout/stderr 存储为 JSON 文件，时间久了可能占满磁盘。
生产环境需要合理配置日志轮转，或使用第三方日志驱动。

## Step 1：查看默认日志驱动

    docker info --format '{{.LoggingDriver}}'
    # 默认: json-file

## Step 2：测试日志输出和轮转

    docker run -d --name log-test \
      --log-opt max-size=1m --log-opt max-file=2 \
      alpine sh -c "while true; do echo 'log line'; done"

查看日志文件的位置：

    docker inspect log-test --format '{{.LogPath}}'
    # 一般是 /var/lib/docker/containers/<ID>/<ID>-json.log
    # Mac 上在 Docker Desktop VM 内部，宿主机不一定能直接访问

等待日志达到 1MB 后，会自动轮转（生成第二个文件）。

## Step 3：不同日志驱动对比

| 驱动 | 特点 | 适合场景 |
|------|------|----------|
| `json-file`（默认）| 文件存储，docker logs 可用 | 单机开发 |
| `local` | 高效存储，自动压缩 | 单机生产 |
| `journald` | 与 systemd 日志整合 | Linux 生产 |
| `fluentd` / `syslog` / `gelf` | 发送到外部日志系统 | 集中式日志 |
| `none` | 不记录日志 | 测试 |

## Step 4：Compose 中的日志配置

    cat 04-logging/compose.yml

## Step 5：体验 local 驱动（更高效）

    docker run --log-driver local alpine echo hello
    docker logs $(docker ps -lq)     # 日志依然可读

## Step 6：日志最佳实践

1. **应用写日志到 stdout/stderr**，不要写到文件——否则 Docker 和编排工具没法采集
2. **设置轮转**：`--log-opt max-size=10m --log-opt max-file=3`
3. **生产环境考虑收集**：用 Fluentd / Loki / Datadog 等将日志集中到外部
4. **敏感信息不要打日志**：密码、Token、密钥

## 清理

    docker rm -f log-test

## 检查清单

- [ ] 理解 Docker 日志驱动体系
- [ ] 知道如何配置日志轮转
- [ ] 理解为什么应用应该写日志到 stdout/stderr

## 思考题

1. 如果 `max-file=3`，当第 4 个日志文件产生时，最旧的那个会被怎样？
2. `local` 驱动和 `json-file` 驱动相比，优势在哪里？
3. 应用直接写日志到文件（如 `/var/log/app.log`）而不是 stdout，Docker 能捕获吗？要怎么处理？
4. Docker Desktop 的日志文件实际存在哪里？
5. Kubernetes 中的日志采集是怎么做的？和 Docker 的日志驱动是什么关系？
6. `docker logs --tail 100 --follow` 会读取存储的日志文件还是实时流？
7. `docker compose logs` 和 `docker logs` 的区别是什么？
8. 如果配置了 `journald` 驱动，`docker logs` 还能用吗？
9. 日志驱动会影响容器性能吗？哪个驱动性能最好？
10. 容器被 `docker rm` 之后，它的日志文件也会被删除吗？
