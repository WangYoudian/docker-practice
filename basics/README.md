
# Phase 1 · 基础命令

Docker 基础操作练习。目标：熟练管理容器的完整生命周期。

## 练习列表

| # | 练习 | 核心概念 | 预计用时 |
|---|------|----------|----------|
| 1 | [Hello World](01-hello-world.md) | 镜像拉取、容器运行、基本概念 | 5 min |
| 2 | [容器生命周期](02-container-lifecycle.md) | run/stop/rm/ps，前台 vs 后台 | 10 min |
| 3 | [端口映射](03-port-mapping.md) | -p 端口暴露、多容器端口 | 10 min |
| 4 | [进入容器与日志](04-exec-and-logs.md) | exec、logs、attach | 10 min |
| 5 | [数据持久化](05-data-persistence.md) | volume、bind mount | 15 min |
| 6 | [资源查看](06-resource-inspection.md) | stats、top、inspect | 10 min |
| 7 | [环境变量](07-environment-variables.md) | -e、env-file | 10 min |

> **建议**：按编号顺序练习，不要跳过。每做完一个在对应标题打 `[x]` 标记进度。

---

**开始前确认 Docker 已安装：**

```bash
docker --version && docker info
```
