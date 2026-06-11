
# 练习 5：镜像瘦身

**目标**：掌握不同基础镜像的选择策略，学会显著减小镜像体积。

**涉及**：`-slim`、`-alpine`、distroless 镜像

---

## Step 1：构建三种版本

    docker build -t python-full -f 05-image-slimming/Dockerfile 05-image-slimming/
    docker build -t python-slim -f 05-image-slimming/Dockerfile.slim 05-image-slimming/
    docker build -t python-alpine -f 05-image-slimming/Dockerfile.alpine 05-image-slimming/

## Step 2：对比大小

    docker images | grep python-

输出类似：

| 版本 | 大小（约）|
|------|----------|
| python:3.11 | ~1GB |
| python:3.11-slim | ~130MB |
| python:3.11-alpine | ~50MB |

## Step 3：理解差异

| 基础镜像 | 特点 | 适合场景 |
|----------|------|----------|
| `python:3.11` 完整版 | 包含编译工具链、文档等 | 需要编译 C 扩展 |
| `python:3.11-slim` | 只保留运行所需的最小系统库 | 大部分 Python 应用 |
| `python:3.11-alpine` | 基于 musl libc，最小但不一定最快 | 简单脚本、体积优先 |

## Step 4：高级选择：distroless

Google 维护的 distroless 镜像更加极致——连 shell 和包管理器都没有：

```dockerfile
FROM gcr.io/distroless/python3
```

**优势**：攻击面最小，镜像最小
**劣势**：没有 shell，`docker exec` 进去几乎什么都做不了，调试困难

## Step 5：体积检查清单

减小镜像体积的标准思路：

1. 选择合适的基础镜像（slim / alpine）
2. 多阶段构建（只保留编译产物）
3. 合理利用 `RUN` 的链式操作（`apt-get update && apt-get install && rm -rf /var/lib/apt/lists/*`）
4. 避免安装不必要的包

    # 坏的写法（产生额外的层）
    RUN apt-get update
    RUN apt-get install -y curl
    RUN rm -rf /var/lib/apt/lists/*

    # 好的写法（一个 RUN + 清理）
    RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

## 清理

    docker rmi python-full python-slim python-alpine

## 检查清单

- [ ] 能说出 slim、alpine、distroless 的区别
- [ ] 能在 Dockerfile 中写出"合并 RUN + 清理"的模式
- [ ] 理解多阶段构建对减小镜像体积的作用

## 思考题

1. alpine 基于 musl libc，slim 基于 glibc，这对 Python 的 wheel 安装有什么影响？
2. distroless 镜像的优势是安全，但缺点也很明显。你会怎么在生产中权衡？
3. `docker history <image>` 命令可以查看镜像每层的大小，试试看。
