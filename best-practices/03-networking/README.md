
# 练习 3：Docker 网络深入

**目标**：理解 Docker 的网络模式，掌握自定义网络的隔离和通信。

**涉及**：bridge / host / none 模式、自定义网络、`docker network`

---

## 背景

容器间的网络通信是生产环境的必备技能。Docker 提供多种网络模式：

| 模式 | 行为 |
|------|------|
| bridge（默认）| 容器在独立网段，通过 NAT 访问外网 |
| host | 容器直接使用宿主机网络栈，无隔离 |
| none | 容器没有网络 |
| custom bridge | 用户自定义网段，支持 DNS 解析 |

## Step 1：三种网络模式的对比

    docker run -d --name net-bridge alpine sleep 100
    docker run -d --name net-host --network host alpine sleep 100
    docker run -d --name net-none --network none alpine sleep 100

对比差异：

    docker exec net-bridge ip addr show
    docker exec net-host ip addr show      # 和宿主机一样
    docker exec net-none ip addr show      # 只有 lo

    docker inspect net-bridge --format '{{.NetworkSettings.IPAddress}}'
    # 能拿到 IP

## Step 2：自定义网络的好处——DNS 解析

默认 bridge 网络只能通过 IP 互通，自定义网络支持通过服务名（容器名）访问。

    docker network create my-net
    docker run -d --name web --network my-net nginx:alpine
    docker run --rm --network my-net alpine wget -qO- http://web
    # 通过容器名 web 就能访问！

默认 bridge 下不行：

    docker run -d --name web2 nginx:alpine
    docker run --rm alpine wget -qO- http://web2
    # 报错：bad address

## Step 3：多网络隔离

    cd 03-networking
    docker compose up -d

查看 compose.yml 中的设计：
- `app1` 只在 `frontend`
- `app2` 同时连 `frontend` 和 `backend`
- `db` 只在 `backend`

验证连通性：

    docker compose exec app1 ping app2     # 通
    docker compose exec app1 ping db       # 不通（不同网络）
    docker compose exec app2 ping db       # 通（app2 在 backend 里）

这就是**网络隔离**：db 对外不可见，只有中间层 app2 能访问。

## Step 4：host 模式的用途

    docker run --network host -d nginx:alpine
    curl http://localhost

没有端口映射，直接访问宿主机 80 端口。适合对网络性能要求极高的场景。
但 host 模式在 Mac 上行为不同（因为 Docker 运行在 VM 中）。

## 清理

    docker rm -f net-bridge net-host net-none web web2
    docker network rm my-net
    docker compose down
    cd ..

## 检查清单

- [ ] 理解 bridge / host / none 三种模式
- [ ] 能在自定义网络中通过容器名通信
- [ ] 理解多网络实现网络隔离

## 思考题

1. 为什么自定义 bridge 支持 DNS 解析而默认 bridge 不支持？
2. 容器能动态加入或离开网络吗？（提示：`docker network connect` / `disconnect`）
3. Mac 的 host 网络模式和 Linux 上的行为有什么不同？为什么？
4. 什么场景适合用 host 模式？什么场景绝对不能用？
5. overlay 网络是给什么场景用的？
