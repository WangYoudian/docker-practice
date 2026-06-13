
# Alpine vs Slim：对 Python wheel 安装的影响

两个基础镜像最核心的差异在于 **C 标准库**：

| | slim | alpine |
|---|---|---|
| libc | glibc | musl |
| 基础 | Debian | Alpine Linux (BusyBox) |
| 体积 | ~120 MB | ~50 MB |
| wheel 标签 | `manylinux` | `musllinux` |

## 为什么影响 wheel 安装

PyPI 上的预编译 wheel 附有平台标签，pip 会检查标签是否匹配当前系统。大多数第三方包只发布 `manylinux`（glibc）的 wheel，Alpine 下会匹配失败而回退到**源码编译**。

## 各场景对比

| 包类型 | slim | alpine |
|--------|------|--------|
| 纯 Python（requests、httpx） | wheel，无感 | wheel，无感 |
| 热门 C 扩展（numpy、cryptography、pandas） | manylinux wheel，直装 | 大多有 musllinux wheel，直装 |
| 冷门 C 扩展（小众数据库驱动、自定义 C 库绑定） | manylinux wheel，直装 | **需编译**，缺 musl-dev/build-base 则失败 |

## 实战建议

- **优先用 slim**：构建快、兼容性好，多出来的几十 MB 镜像体积在 CI 构建时间上通常能省回来
- **确定要用 alpine 的场景**：
  - 部署环境本身是 alpine（如 K3s、某些嵌入式场景）
  - 镜像体积有严格限制（几十 MB 的差距确实关键）
  - 项目中无或少 C 扩展依赖
- **用 alpine 时**：Dockerfile 里提前装好编译工具链，并用好缓存层避免每次重编

```dockerfile
# 如果要走 alpine，提前装好编译工具
FROM python:3.11-alpine
RUN apk add --no-cache build-base musl-dev
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
```

## 延伸阅读

- PEP 656 — musllinux 平台标签（2021）
- PEP 599 — manylinux 平台标签
- Python wheels 官方说明

> 这份笔记讨论的是 linux/amd64 和 linux/arm64 的情况，macOS/Windows 的 wheel 标签体系不同。
