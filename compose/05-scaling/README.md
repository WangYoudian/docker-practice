
# 练习 5：水平扩展

**目标**：用 `--scale` 实现服务的水平扩展，并用 Nginx 做负载均衡。

**涉及**：`--scale`、`ports` 冲突解决、Nginx 反向代理

---

## Step 1：查看项目文件

    cat 05-scaling/compose.yml
    cat 05-scaling/nginx.conf

两个服务：
- `app`：Python 简单服务，返回容器 hostname
- `nginx`：反向代理，把请求转发给 `app` 服务

注意 `app` 服务没有 `ports` 映射——因为应用内部通过 Nginx 访问，不需要暴露到宿主机。

## Step 2：启动并扩展

    cd 05-scaling
    docker compose up -d --scale app=3

`--scale app=3` 会创建 3 个 app 容器实例。Compose 会自动为它们分配不同的 hostname。

## Step 3：验证负载均衡

    curl http://localhost:8105
    # Served by: 05-scaling-app-1-xxx

    for i in $(seq 1 6); do curl -s http://localhost:8105; done

每次请求由不同的实例处理（Nginx 默认 round-robin），hostname 会轮换。

## Step 4：查看扩展后的状态

    docker compose ps
    # app 服务有 3 个容器

## Step 5：动态调整规模

    docker compose up -d --scale app=5
    docker compose ps | grep app
    # 可以看到 5 个 app 容器

    docker compose up -d --scale app=2
    docker compose ps | grep app
    # 多余的容器被自动移除

## 清理

    docker compose down
    cd ..

## 检查清单

- [ ] 理解 `--scale` 的用法
- [ ] 知道扩展无状态服务时需要 Nginx 做负载均衡
- [ ] 理解为什么扩展的服务不应该用 `ports` 直接暴露

## 思考题

1. 为什么扩展 `app` 服务时不能给它加 `ports` 映射？（提示：端口冲突）
2. Nginx 配置中的 `upstream` block 做了什么？Compose 的服务发现如何让 Nginx 找到多个 `app` 实例？
3. `--scale app=0` 会发生什么？
4. Compose 的 `deploy.replicas` 和 `--scale` 是什么关系？在 swarm 模式下会怎样？

---

**Phase 3 练习全部完成！可以进入 [Phase 4：最佳实践](../best-practices/README.md)**
