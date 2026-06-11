
# Phase 4 · 最佳实践

目标：把容器化应用推向生产级别——安全、可靠、可观测、可维护。

## 练习列表

| # | 练习 | 核心概念 | 预计用时 |
|---|------|----------|----------|
| 1 | [非 root 运行](01-non-root/README.md) | USER 指令、安全上下文 | 10 min |
| 2 | [资源限制](02-resource-limits/README.md) | memory/cpu/restart 策略 | 10 min |
| 3 | [网络深入](03-networking/README.md) | bridge/host 模式、自定义网络 | 15 min |
| 4 | [日志策略](04-logging/README.md) | 日志驱动、轮转配置 | 10 min |
| 5 | [多架构构建](05-multi-arch/README.md) | buildx、多平台镜像 | 15 min |
| 6 | [安全扫描](06-security/README.md) | Trivy 扫描、常见漏洞 | 10 min |
| 7 | [CI/CD 集成](07-cicd/README.md) | Makefile、GitHub Actions | 15 min |

---

> Phase 4 的练习建立在 Phase 1-3 的知识之上，建议顺序完成。
> 部分练习需要安装额外工具（Trivy、buildx 等），会在对应章节说明。
