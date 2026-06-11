
# 练习 5：多架构镜像（buildx）

**目标**：学会使用 `docker buildx` 构建多平台镜像，在 Apple Silicon 和 x86 架构间自由切换。

**涉及**：`buildx`、`--platform`、QEMU 模拟

---

## 背景

Apple Silicon (arm64) 和服务器 (amd64) 架构不同。如果一个镜像只构建了 amd64，
在 Mac 上运行可能会慢（通过 QEMU 模拟）甚至不兼容。

**目标**：一次构建，多架构运行。

## Step 1：检查当前环境

    docker info --format '{{.Architecture}}'
    # Apple Silicon: aarch64 / arm64
    # Intel Mac: x86_64

    docker buildx version
    # buildx 现在已内置在 Docker 中

    docker buildx ls
    # 查看可用的构建器和支持的平台

## Step 2：构建单一平台

    docker build --platform linux/amd64 -t multi-demo:amd64 05-multi-arch/
    docker build --platform linux/arm64 -t multi-demo:arm64 05-multi-arch/

    docker run --rm multi-demo:amd64
    # 输出: Hello from x86_64

    docker run --rm multi-demo:arm64
    # 输出: Hello from aarch64

## Step 3：构建多架构清单（manifest）

    docker buildx build --platform linux/amd64,linux/arm64 \
      -t multi-demo:latest 05-multi-arch/
    # 会报错，因为默认输出到 docker 镜像存储，不支持多架构
    # 需要 --push 到 registry，或者用 --load 到本地（但 --load 只支持单平台）

如果要保存到本地，可以创建自定义构建器并启用：

    docker buildx create --name mybuilder --use
    docker buildx inspect --bootstrap

然后构建并加载单一架构到本地：

    docker buildx build --platform linux/arm64 -t multi-demo:local --load 05-multi-arch/
    docker run --rm multi-demo:local

## Step 4：查看镜像的 manifest 信息

    docker buildx imagetools inspect multi-demo:latest 2>/dev/null || \
      echo "push 到 registry 后才能看到多架构 manifest"

## 清理

    docker buildx rm mybuilder 2>/dev/null
    docker rmi multi-demo:amd64 multi-demo:arm64 multi-demo:local 2>/dev/null

## 检查清单

- [ ] 理解 arm64 和 amd64 架构差异
- [ ] 知道 `buildx` 的作用
- [ ] 能用 `--platform` 构建特定平台镜像
- [ ] 理解多架构 manifest 的概念

## 思考题

1. 为什么 `docker buildx build --platform ... --load` 不支持多架构到本地存储？
2. QEMU 模拟在 arm64 上跑 amd64 容器有什么性能损失？
3. Docker Hub 上的 `--platform linux/amd64` 和 `linux/arm64` 是用户手动构建的，还是自动的？
4. 如果你维护一个开源项目，如何用 GitHub Actions 自动构建并推送多架构镜像？
5. Apple Silicon 上的 Docker 默认会拉取 arm64 镜像还是 amd64？
6. `FROM --platform=$BUILDPLATFORM` 和 `FROM alpine:3.20` 有什么区别？
7. CI 构建多架构镜像时，通常会用交叉编译还是用 QEMU？
8. `docker build --load` 和 `docker buildx build --load` 的区别是什么？
9. `--platform linux/amd64,linux/arm64` 能包含 `linux/arm/v7`（树莓派）吗？
10. 如果只构建 `linux/amd64`，在 Apple Silicon Mac 上用 Docker Desktop 运行会怎样？
