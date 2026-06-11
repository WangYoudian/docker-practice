
# 练习 6：镜像安全扫描

**目标**：学会使用 Trivy 扫描镜像中的安全漏洞，理解常见的安全问题。

**涉及**：Trivy、Docker Scout、镜像层分析、CVE

---

## 背景

容器镜像中的基础镜像和依赖库可能包含已知漏洞（CVE）。定期扫描是安全基线。

## Step 1：准备扫描工具

推荐使用 Aqua Security 的 **Trivy**（开源且快）：

    brew install trivy

或者使用 Docker Scout（Docker Desktop 内置）：

    docker scout version

## Step 2：拉取一个测试镜像并扫描

    docker pull python:3.11
    trivy image python:3.11

输出会列出所有已知漏洞（按严重程度排列：CRITICAL > HIGH > MEDIUM > LOW）。

如果使用 Docker Scout：

    docker scout quickview python:3.11

## Step 3：对比不同基础镜像的漏洞数

    trivy image python:3.11      # 完整版
    trivy image python:3.11-slim  # slim 版

你会发现 slim 镜像的漏洞远少于完整版。

## Step 4：扫描你自己构建的镜像

    docker build -t my-app 01-non-root/
    trivy image my-app

## Step 5：Trivy 的常用模式

    trivy image --severity CRITICAL,HIGH python:3.11  # 只看高严重性
    trivy image --ignore-unfixed python:3.11           # 只看有修复的漏洞
    trivy image --format table python:3.11             # 表格输出（默认）
    trivy image --format json python:3.11              # JSON 输出

## Step 6：安全最佳实践清单

1. **选择小的基础镜像**：alpine / slim / distroless → 攻击面更小
2. **非 root 运行**：使用 `USER` 指令
3. **定期扫描**：CI 中集成 Trivy 扫描
4. **最小化安装**：不要装不必要的包
5. **多阶段构建**：只拷贝编译产物，不带编译工具链
6. **固定基础镜像版本**：用 `python:3.11-slim` 而不是 `python:latest`
7. **不存储敏感信息**：密码/密钥通过环境变量或 secret 管理
8. **只读文件系统**：`docker run --read-only`
9. **capability 最小化**：`docker run --cap-drop ALL --cap-add NET_BIND_SERVICE`
10. **使用内容信任**：`DOCKER_CONTENT_TRUST=1` 验证镜像签名

## 检查清单

- [ ] 会安装并使用 Trivy 扫描镜像
- [ ] 理解 CVE 和严重性等级
- [ ] 知道如何选择漏洞更少的基础镜像
- [ ] 了解容器安全的 10 条最佳实践

## 思考题

1. 漏洞扫描结果显示 CRITICAL 级别漏洞，是否必须立刻升级基础镜像？需要考虑什么？
2. distroless 镜像的漏洞为什么比 alpine 还少？它有什么权衡？
3. CI 流水线中，扫描发现 CRITICAL 漏洞时应该阻断构建吗？
4. Docker Content Trust 和 Notary 是什么关系？
5. `docker scout` 和 `trivy` 的工作方式有什么不同？哪个更适合 CI？
6. 什么是"基础镜像漏洞传递"？如果 alpine:3.20 有 CVE，基于它的镜像都有吗？
7. `docker run --cap-drop ALL --cap-add NET_BIND_SERVICE` —— 这里的 capability 是什么概念？
8. Docker 的 seccomp 和 AppArmor 是做什么的？
9. 在 CI 中集成镜像扫描时，通常会设置一个"漏洞阈值"（如不允许超过 5 个 HIGH），但这个阈值应该怎么定？
10. 如果基础镜像的历史漏洞在 scan 时被认为是已修复的，但实际编译产物中使用了旧版动态链接库，扫描能发现吗？
