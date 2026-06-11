
# 练习 2：资源限制与重启策略

**目标**：学会给容器设置 CPU/内存限制和重启策略，防止单个容器吃光宿主机。

**涉及**：`--memory`、`--cpus`、`--restart`、Compose 的 `deploy.resources`

---

## 背景

不加限制的容器可能消耗宿主机的所有资源，影响其他进程。Docker 提供了 cgroup 层面的限制。

## Step 1：构建测试镜像

    docker build -t stress-test 02-resource-limits/

## Step 2：不加限制跑 CPU 密集型任务

    docker run --rm -e STRESS_MODE=cpu stress-test
    time docker run --rm stress-test

记录耗时。现在加限制：

    docker run --rm --cpus=0.5 -e STRESS_MODE=cpu stress-test
    time docker run --rm --cpus=0.5 stress-test

限制一半 CPU 后，耗时应该大约是原来的 2 倍。

## Step 3：内存限制

    docker run --rm -e STRESS_MODE=memory -m 256M stress-test
    # 内存逐渐增加直到被 OOM kill

查看容器退出状态：

    docker ps -a --filter name=hungry_ --format '{{.ID}} {{.Status}}'
    docket inspect <ID> --format '{{.State.OOMKilled}}'
    # 如果被 OOM kill，返回 true

## Step 4：重启策略

    docker run -d --name always-up --restart unless-stopped alpine sleep 30
    docker kill always-up
    # 会自动重启

| 策略 | 行为 |
|------|------|
| `no` | 不自动重启（默认）|
| `on-failure` | 退出码非 0 时重启 |
| `unless-stopped` | 除非手动 stop，否则总重启 |
| `always` | 总是重启 |

## Step 5：Compose 中的资源限制

    cat 02-resource-limits/compose.yml

注意 `deploy.resources` 在 docker compose 中只在 swarm 模式下生效。
单机模式可以试 `docker compose up -d`，但限制不会生效——单机用 `--memory` 参数。

## 清理

    docker rm -f always-up
    docker rmi stress-test

## 检查清单

- [ ] 能用 `--cpus` 和 `--memory` 限制容器资源
- [ ] 理解 OOM kill 机制
- [ ] 知道四种 `--restart` 策略的区别

## 思考题

1. 如果 `--memory=256M` 限制下，容器尝试分配 300MB，会发生什么？OOM 还是报错？
2. `--memory-reservation` 和 `--memory` 有什么区别？
3. `docker stats` 看到的内存使用超过了 `--memory` 限制，这正常吗？
4. Kubernetes 的 `resources.limits` 和 `resources.requests` 和这里的 `limits` / `reservations` 是什么关系？
5. `docker run --restart=always` 和 systemd 的 `Restart=always` 有什么异同？
