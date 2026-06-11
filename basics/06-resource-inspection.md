
# 练习 6：资源查看与容器诊断

**目标**：学会监控容器的 CPU、内存、网络等资源使用情况，以及用 inspect 查看容器详细信息。

**涉及命令**：`docker stats`、`docker top`、`docker inspect`

---

## Step 1：启动一个"吃资源"的容器

```bash
docker run -d --name stresser alpine sh -c "while true; do :; done"
```

这个容器会跑一个无限循环，持续占用 CPU。

## Step 2：查看容器内的进程

```bash
docker top stresser
```

你会看到容器内的进程列表，PID（容器视角）和宿主机视角的 PID 都能看到。

## Step 3：实时查看资源占用

```bash
docker stats
```

会显示一个类似 `top` 的实时面板，包含：

- CPU % — CPU 使用率
- MEM USAGE / LIMIT — 内存使用
- NET I/O — 网络流量
- BLOCK I/O — 磁盘读写
- PIDS — 进程数

按 `Ctrl+C` 退出。

只看某个容器的资源：
```bash
docker stats stresser
```

## Step 4：用 inspect 查看容器的元数据

`docker inspect` 返回完整的 JSON 信息：

```bash
docker inspect stresser
```

输出很长，可以用 `--format` 提取特定字段：

```bash
# 查看容器状态
docker inspect stresser --format '{{.State.Status}}'

# 查看容器 IP 地址
docker inspect stresser --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'

# 查看挂载的 volumes
docker inspect stresser --format '{{json .Mounts}}' | jq .

# 查看容器启动命令
docker inspect stresser --format '{{.Name}} {{.Config.Cmd}}'
```

> 如果没装 `jq`，可以用 Python：`docker inspect stresser | python3 -m json.tool`

## Step 5：查看容器事件

Docker 会记录所有容器的生命周期事件：

```bash
# 另开一个终端执行
docker events &

# 在当前终端做点操作
docker run --rm alpine echo hello
docker ps
```

可以看到 `create`、`start`、`die` 等事件实时输出。

## Step 6：对比两个不同负载的容器

```bash
docker run -d --name idle alpine sleep 9999

# 对比 idel vs stresser
docker stats stresser idle
```

## 清理

```bash
docker rm -f stresser idle
```

## 检查清单

- [ ] 能用 `docker stats` 实时监控资源使用
- [ ] 能用 `docker top` 查看容器内进程
- [ ] 能用 `docker inspect` 查看完整元数据
- [ ] 能用 `--format` 提取 JSON 中的特定字段
- [ ] 知道 `docker events` 的存在

## 思考题

1. `docker stats` 显示的 CPU% 是占宿主机的百分比还是占容器配额的比例？
2. 如果不限制容器的资源，一个容器能把宿主机的 CPU 吃满吗？
3. `docker inspect` 的 `--format` 用了 Go template 语法。除了 `{{.XXX}}`，Go template 还支持哪些控制结构？
