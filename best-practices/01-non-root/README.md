
# 练习 1：非 root 运行

**目标**：理解为什么容器不应该以 root 运行，以及如何在 Dockerfile 中创建并切换到非 root 用户。

**涉及**：`RUN adduser`、`USER` 指令

---

## 背景

默认情况下容器以 root 运行。如果攻击者通过漏洞逃逸到宿主机，root 权限可能导致灾难。
此外，以 root 写入的文件在宿主机上也是 root 所有的，会引起权限问题。

**好习惯**：镜像里创建专用用户，用 `USER` 切换。

## Step 1：对比两个 Dockerfile

    cat 01-non-root/Dockerfile.bad   # 以 root 运行
    cat 01-non-root/Dockerfile       # 创建 appuser 并切换

好的 Dockerfile 做了三件事：
1. 用 `addgroup` / `adduser` 创建非 root 用户
2. 用 `USER appuser` 切换
3. 注意 `WORKDIR` 在 `USER` **之前**（否则 appuser 可能没有目录写入权限）

## Step 2：构建并验证

    docker build -t non-root -f 01-non-root/Dockerfile 01-non-root/
    docker run --rm -d -p 9001:8000 --name non-root-demo non-root
    curl http://localhost:9001
    # 输出: Running as: appuser (UID: 1000)

## Step 3：验证容器内确实不是 root

    docker exec non-root-demo whoami
    # 输出: appuser

## Step 4：对比以 root 运行的版本

    docker build -t root-run -f 01-non-root/Dockerfile.bad 01-non-root/
    docker run --rm -d -p 9002:8000 --name root-demo root-run
    docker exec root-demo whoami
    # 输出: root (UID: 0)

## Step 5：如果是 bind mount，root 的文件权限问题

    mkdir -p /tmp/root-test
    docker run --rm -v /tmp/root-test:/data alpine touch /data/test.txt
    ls -la /tmp/root-test/test.txt
    # 文件所有者是 root，普通用户删不掉

如果用普通用户：

    docker run --rm -u 1000:1000 -v /tmp/root-test:/data alpine touch /data/test2.txt
    ls -la /tmp/root-test/test2.txt
    # 文件所有者为 UID 1000

## 清理

    docker rm -f non-root-demo root-demo
    rm -rf /tmp/root-test
    docker rmi non-root root-run

## 检查清单

- [ ] 理解为什么容器不应以 root 运行
- [ ] 能在 Dockerfile 中创建用户并切换
- [ ] 知道 `addgroup` / `adduser` 的语法
- [ ] 知道 bind mount 时 root 写入的副作用

## 思考题

1. 如果应用需要访问特权端口（如 80），用非 root 用户怎么处理？
2. `USER 1000:1000` 和 `USER appuser` 有什么区别？
3. Docker 的 `--user` 运行时参数和 Dockerfile 的 `USER` 指令，哪个优先级高？
4. Kubernetes 中的 `securityContext.runAsNonRoot: true` 和 Docker 的 `USER` 是什么关系？
5. 有些基础镜像（如 `gcr.io/distroless`）默认没有 shell 也没有包管理器，那还能 `adduser` 吗？
