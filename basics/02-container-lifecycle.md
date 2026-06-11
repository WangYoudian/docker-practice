
# 练习 2：容器生命周期管理

**目标**：掌握容器的完整生命周期：创建 → 启动/停止 → 杀死 → 删除。

**涉及命令**：`docker run`、`docker start`、`docker stop`、`docker kill`、`docker rm`

---

## Step 1：后台运行一个容器

启动一个 Nginx 容器，在后台运行：

```bash
docker run -d --name my-nginx nginx:alpine
```

参数说明：
- `-d`：后台运行（detached）
- `--name`：给容器起名，方便后续操作
- `nginx:alpine`：基于 Alpine 的极简 Nginx 镜像

## Step 2：查看运行中的容器

```bash
docker ps
```

看到 `my-nginx` 状态为 `Up`。注意 `NAMES` 列和 `CONTAINER ID`。

## Step 3：停止容器

```bash
docker stop my-nginx
```

Docker 会发送 SIGTERM，等待超时后发送 SIGKILL。再次运行 `docker ps`，容器已经不在了。

```bash
# 但用 -a 还能看到，状态变成了 Exited
docker ps -a
```

## Step 4：重启已停止的容器

```bash
docker start my-nginx
docker ps          # 确认状态变回 Up
```

## Step 5：强制杀死容器

```bash
docker kill my-nginx
```

`kill` 直接发 SIGKILL，不给优雅关闭的机会。比 `stop` 更暴力。

## Step 6：删除容器

```bash
# 先确认是 stopped 状态
docker ps -a | grep my-nginx

docker rm my-nginx
docker ps -a       # 确认已删除
```

如果容器正在运行，需要先 stop 或加 `-f` 强制删除：

```bash
docker run -d --name test-rm nginx:alpine
docker rm -f test-rm   # 强制删除运行中的容器
```

## Step 7：一次性容器（退出后自动删除）

```bash
docker run --rm alpine echo "I will be deleted after exit"
docker ps -a       # 看不到这个容器
```

`--rm` 非常适合临时测试，容器退出后自动清理，不给 `ps -a` 添乱。

## 清理

```bash
# 删除所有已停止的容器
docker container prune

# 或者只删指定的
docker rm my-nginx test-rm 2>/dev/null
```

## 检查清单

- [ ] 能熟练使用 `run -d` 后台启动容器
- [ ] 分清 `stop`（优雅）和 `kill`（暴力）的区别
- [ ] 知道已停止的容器可以 `start` 重启
- [ ] 知道 `--rm` 参数的作用

## 思考题

1. 一个容器 stop 之后，文件系统里的修改还在吗？如果 rm 之后呢？
2. 如果 `docker run` 时不指定 `--name`，Docker 会怎么命名？
3. `docker container prune` 和 `docker rm $(docker ps -aq)` 有什么区别？
