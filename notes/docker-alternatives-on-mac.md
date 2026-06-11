
# Docker 替代品调研：Podman / nerdctl / Lima 在 Mac 上的对比

> 调研时间：2025年6月
> 环境：macOS (Apple Silicon)

## 背景

Docker Desktop 在 2021 年对大型企业收费后，社区开始寻找替代方案。
目前主流的选择集中在 **Podman**、**nerdctl + Lima**、**Colima** 和 **Finch**。

## 定位差异

```
┌──────────────────────────────────────────────┐
│                 容器生态分层                     │
├──────────────────────────────────────────────┤
│  CLI 层     podman / nerdctl / docker         │
│  ──────────────────────────────────────────  │
│  运行时层    containerd / dockerd / crun/runc  │
│  ──────────────────────────────────────────  │
│  VM 层      Lima / podman-machine             │
│  ──────────────────────────────────────────  │
│  宿主机     macOS (需要 Linux VM 才能跑容器)    │
└──────────────────────────────────────────────┘
```

**关键理解**：Lima 在 VM 层，Podman 和 nerdctl 在 CLI 层，它们不是平级竞争关系，但可以互相搭配。

---

## 各工具详解

### Podman

Red Hat 出品，最直接的 Docker 替代。

| 维度 | 说明 |
|------|------|
| 架构 | 无守护进程，每个容器是直接子进程 |
| rootless | 原生支持，普通用户即可运行 |
| Docker 兼容 | 极高，`alias docker=podman` 基本可用 |
| Pod 管理 | 原生支持 Kubernetes 风格的 Pod |
| Mac 原理 | 通过 `podman machine` 启动 Linux VM（qemu/libkrun）|
| Apple Silicon | 良好 |
| 安装复杂度 | 低：`brew install podman` → `podman machine init && start` |

**适合场景**：希望最接近 Docker 体验、需要 rootless 安全的场景。

---

### nerdctl

containerd 项目的官方 Docker 兼容 CLI。

| 维度 | 说明 |
|------|------|
| 架构 | CLI 调用 containerd 运行时 |
| rootless | 否（VM 内 root），但 containerd 本身支持 |
| Docker 兼容 | 高，docker-compose、build 等子命令都有 |
| 额外能力 | 镜像加密、lazy pulling、OCI 制品管理 |
| Mac 原理 | 必须配合 Linux VM，通常搭配 Lima |
| Apple Silicon | 很好（通过 Lima 的 vz 模式）|
| 安装复杂度 | 中：需要理解 Lima + containerd + nerdctl 三层 |

```bash
brew install lima
limactl start template://nerdctl
alias docker="lima nerdctl"
```

**适合场景**：已在用 containerd（如 Kubernetes 节点），想统一开发/生产环境。

---

### Lima

可以理解为 **"macOS 上的 WSL2"**。

| 维度 | 说明 |
|------|------|
| 定位 | Linux VM 管理器，本身不是容器引擎 |
| Mac 原理 | 使用 Apple Virtualization.framework (vz) 或 QEMU |
| 文件共享 | virtiofs，读写性能接近原生 |
| 启动速度 | 几秒钟 |
| 可搭配模板 | docker / nerdctl / k8s 等多种 |
| 资源占用 | 低 |

```bash
brew install lima
limactl start docker          # VM 内跑 Docker
limactl start template://nerdctl  # VM 内跑 containerd
```

**适合场景**：需要轻量 Linux VM，或想自选容器引擎后端。

---

### Colima

基于 Lima 的上层封装，更"傻瓜式"。

```bash
brew install colima
colima start      # 自动启动 Lima VM + containerd
```

灵活性不如直接操作 Lima，但开箱即用。

---

### Finch（AWS 出品）

Lima + nerdctl + containerd 的打包发行版。

```bash
brew install finch
finch vm init
finch run nginx:latest
```

AWS 内部用，社区较小。

---

## 总体对比

| 维度 | Podman | nerdctl + Lima | Colima | Finch |
|------|--------|----------------|--------|-------|
| 底层运行时 | crun (自研) | containerd | containerd | containerd |
| Mac 需要 VM | podman-machine | Lima | Lima | Lima |
| Docker 兼容 | ★★★★★ | ★★★★ | ★★★★ | ★★★★ |
| rootless 原生 | 是 | 否 (VM 内) | 否 | 否 |
| Apple Silicon | 好 | 很好 (vz) | 很好 (vz) | 很好 (vz) |
| 安装复杂度 | 低 | 中 | 低 | 低 |
| 社区活跃度 | 很高 | 中 | 中 | 中低 |

---

## 建议

1. **学习阶段继续用 Docker**——资料最多、生态最成熟、适合打基础
2. 学完后装 **Podman** 试试，`alias docker=podman` 跑通之前所有练习
3. 想深入理解 Mac 容器原理，试试 **Lima + nerdctl**，能理解 VM 层和运行时层的分工
4. 容器核心概念（镜像、层、网络、卷）在所有工具里是通用的，换了工具不必重新学
