
# Phase 2 · Dockerfile 实践

目标：从零写出高效、安全、可复用的 Dockerfile。

## 练习列表

| # | 练习 | 核心概念 | 预计用时 |
|---|------|----------|----------|
| 1 | [第一个 Dockerfile](01-first-dockerfile/README.md) | FROM / COPY / CMD，构建并运行 | 10 min |
| 2 | [构建上下文](02-build-context/README.md) | .dockerignore、上下文体积控制 | 10 min |
| 3 | [分层缓存](03-layer-caching/README.md) | 指令顺序优化、缓存命中策略 | 10 min |
| 4 | [多阶段构建](04-multi-stage/README.md) | 编译与运行阶段分离 | 15 min |
| 5 | [镜像瘦身](05-image-slimming/README.md) | alpine / slim / distroless 对比 | 10 min |
| 6 | [ENTRYPOINT vs CMD](06-entrypoint-cmd/README.md) | 两种指令的组合用法 | 10 min |
| 7 | [健康检查](07-healthcheck/README.md) | HEALTHCHECK 与容器监控 | 10 min |

> **建议**：顺序练习。每个练习目录下都有实际可构建的 Dockerfile 和源码。

---

**检查 Dockerfile 语法：**

```bash
docker run --rm -v $(pwd):/workspace hadolint/hadolint /workspace/Dockerfile
```
