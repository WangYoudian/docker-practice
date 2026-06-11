
# Phase 3 · Docker Compose

目标：用 Compose 编排真实的多容器应用。

## 练习列表

| # | 练习 | 核心概念 | 预计用时 |
|---|------|----------|----------|
| 1 | [Web + Redis](01-web-redis/README.md) | 服务定义、网络联通 | 15 min |
| 2 | [Web + PostgreSQL](02-web-db/README.md) | 数据持久化、初始化脚本 | 15 min |
| 3 | [依赖与健康检查](03-dependencies/README.md) | depends_on + condition | 10 min |
| 4 | [多环境配置](04-multi-env/README.md) | override、多文件 Compose | 15 min |
| 5 | [水平扩展](05-scaling/README.md) | --scale、负载均衡 | 15 min |

---

**开始前确认已安装 Compose 插件：**

    docker compose version
# Docker Desktop 和 Compose 插件默认已捆绑，无需单独安装
