
# 练习 1：Hello World

**目标**：理解 Docker 的基本工作流程：拉取镜像 → 运行容器 → 查看容器。

**涉及命令**：`docker pull`、`docker run`、`docker ps`、`docker images`

---

## Step 1：运行一个快速测试容器

```bash
docker run hello-world
```

观察输出。你会看到一条欢迎消息，Docker 告诉你它尝试拉取 `hello-world` 镜像，然后创建并运行了一个容器。

> **思考**：你的机器上之前有 `hello-world` 这个镜像吗？Docker 在哪里找到了它？

## Step 2：查看本地镜像

```bash
docker images
```

你应该看到 `hello-world` 出现在列表中。

## Step 3：查看容器（包括已退出的）

```bash
# 只看运行中的容器
docker ps

# 查看所有容器（包括已停止的）
docker ps -a
```

`hello-world` 容器打印完消息后就退出了，所以 `docker ps` 看不到它，但 `docker ps -a` 能看到。

## Step 4：手动拉取镜像（不立即运行）

```bash
docker pull alpine
```

这会拉取一个极小的 Linux 镜像（只有 5MB 左右）。运行 `docker images` 确认它已下载。

## Step 5：交互式运行 alpine

```bash
docker run -it alpine sh
```

你现在已经进入容器内部的 shell 了！可以试试：

```bash
cat /etc/os-release   # 查看系统版本
ls /                  # 查看文件系统
exit                  # 退出容器
```

退出后，容器也会停止。

## 清理

```bash
docker ps -a          # 查看所有容器
docker rm <CONTAINER_ID>  # 删除指定容器
# 或者一键删除所有已停止的容器：
docker container prune

docker rmi hello-world alpine  # 删除镜像（可选）
```

## 检查清单

- [ ] 理解了 `docker pull` 和 `docker run` 的区别
- [ ] 知道 `docker images` 查看本地镜像
- [ ] 知道 `docker ps` vs `docker ps -a` 的区别
- [ ] 成功进入过一个容器的 shell 并退出

## 思考题

1. 当你运行 `docker run hello-world` 时，如果不先 `docker pull`，Docker 会怎么做？
2. `docker run -it alpine sh` 中的 `-it` 是什么意思？（提示：`-i` + `-t`）
