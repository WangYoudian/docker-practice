
# 练习 4：进入容器与日志

**目标**：学会进入容器内部调试、查看容器日志。

**涉及命令**：`docker exec`、`docker logs`、`docker attach`

---

## Step 1：启动一个后台容器

```bash
docker run -d --name my-server nginx:alpine
```

## Step 2：查看实时日志

```bash
# 查看全部日志
docker logs my-server

# 实时跟踪日志（类似 tail -f）
docker logs -f my-server
```

保持 `logs -f` 运行，另开一个终端：

```bash
curl http://localhost:80
```

回到第一个终端，能看到访问日志实时出现。按 `Ctrl+C` 退出跟踪。

其他常用参数：
```bash
docker logs --tail 10 my-server   # 只看最后10行
docker logs --since 5m my-server  # 只看过去5分钟
docker logs -t my-server          # 显示时间戳
```

## Step 3：在运行中的容器里执行命令

```bash
# 在容器里执行一条命令，查看其进程
docker exec my-server ps aux

# 查看容器内的 Nginx 配置
docker exec my-server cat /etc/nginx/nginx.conf
```

## Step 4：交互式进入容器 shell

```bash
docker exec -it my-server sh
```

进去之后可以像操作一台小机器一样：

```bash
ls -la /usr/share/nginx/html/   # Nginx 的静态文件目录
cat /etc/os-release             # Alpine Linux
ps aux                          # 查看容器内进程
hostname                        # 容器的主机名 = 容器 ID
exit
```

> **注意**：为什么是 `sh` 而不是 `bash`？因为 Alpine 镜像只有 `sh` (BusyBox)，没有 bash。

## Step 5：exec 与 attach 的区别

```bash
# 启动一个长期运行的后台进程
docker run -d --name looper alpine sh -c "while true; do echo 'alive'; sleep 2; done"

# attach 到容器的主进程（PID 1）
docker attach looper
# 按 Ctrl+C, 容器会停止（因为主进程收到了 SIGINT）
```

`attach` 是连接到容器的主进程，而 `exec` 是创建**新的**进程。

## 清理

```bash
docker rm -f my-server looper
```

## 检查清单

- [ ] 能用 `docker logs -f` 实时查看日志
- [ ] 能用 `docker exec` 在容器内执行单条命令
- [ ] 能用 `docker exec -it` 进入容器 shell
- [ ] 理解 `exec` 和 `attach` 的区别

## 思考题

1. 如果容器里没有 `sh` 或 `bash`（比如 `scratch` 镜像），还能 `docker exec -it` 吗？
2. `docker logs` 能查看已停止容器的日志吗？试试看。
3. 如果你的应用日志写到文件而不是 stdout，Docker 能捕获到吗？怎么解决？
