
# 练习 7：CI/CD 集成

**目标**：学会用 Makefile 和 GitHub Actions 自动化镜像构建、扫描和发布。

**涉及**：Makefile、GitHub Actions、Docker Buildx、Trivy

---

## 背景

手动 `docker build` 和 `docker push` 在开发阶段没问题，但生产环境需要自动化的 CI/CD。

## Step 1：使用 Makefile 管理本地构建

    cat 07-cicd/Makefile

常用命令：

    cd 07-cicd
    make build    # 构建镜像
    make lint     # 用 hadolint 检查 Dockerfile 质量
    make test     # 验证镜像能正常运行
    make scan     # 扫描 CRITICAL 漏洞（需要安装 trivy）
    make all      # 一条命令做完上面所有步骤

## Step 2：使用 hadolint 检查 Dockerfile

Hadolint 能自动检查 Dockerfile 的常见问题：

    docker run --rm -v $(PWD)/Dockerfile:/Dockerfile:ro hadolint/hadolint /Dockerfile

它会提示：没用 `WORKDIR`、`apt-get` 后没清理、基础镜像版本没固定等。

## Step 3：理解 GitHub Actions Workflow

    cat 07-cicd/.github/workflows/docker.yml

这个 workflow 有 3 个 job：

1. **lint**：用 hadolint 检查 Dockerfile 规范
2. **build-and-scan**：构建镜像并用 Trivy 扫描 CRITICAL 漏洞
3. **publish**（仅在打 tag 时触发）：构建多架构镜像并推送到 GitHub Container Registry

## Step 4：在自己的项目中使用

把 `07-cicd/.github/workflows/docker.yml` 复制到项目的 `.github/workflows/docker.yml`，
基于 `07-cicd/Makefile` 修改成自己项目的配置，然后推送到 GitHub 即可自动执行。

## 检查清单

- [ ] 理解 Makefile 中 .PHONY 的作用
- [ ] 知道 hadolint 是什么
- [ ] 理解 GitHub Actions 的 job 结构和触发条件
- [ ] 理解 CI/CD 流水线中 lint -> scan -> test -> publish 的顺序

## 思考题

1. Makefile 中 `.PHONY` 有什么用？不写会有什么问题？
2. GitHub Actions 的 `needs: [lint, build-and-scan]` 在 pipeline 中起什么作用？
3. `docker/build-push-action@v5` 的 `load: true` 和 `push: true` 有什么区别？
4. 为什么不直接把 `docker push` 写在 `on: push` 而只写在 `on: push tags` 上？
5. 如果 CI 中 Trivy 扫描出了漏洞，pipeline 应该阻断发布还是仅告警？
6. `secrets.GITHUB_TOKEN` 是自动注入的吗？它的权限范围是什么？
7. 除了 GitHub Actions，还有哪些 CI/CD 工具对 Docker 构建有良好的支持？

---

Phase 4 练习全部完成！整个 Docker Practice 课程到此结束。
