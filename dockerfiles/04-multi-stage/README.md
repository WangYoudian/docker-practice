
# 练习 4：多阶段构建

**目标**：理解多阶段构建的原理，掌握编译与运行阶段分离的技巧。

**涉及**：`AS` 命名阶段、`COPY --from`、`--target`

---

## 背景

Go、Java、Rust 等语言需要编译。如果用一个完整的编译器镜像构建，编译工具链和源码都会留在最终镜像里，导致镜像很大。

多阶段构建允许你定义多个 `FROM`，最终产物只拷贝到最后一个阶段。

## Step 1：查看多阶段 Dockerfile

    cat 04-multi-stage/Dockerfile

两个阶段：

1. **builder**：用 `golang:1.22-alpine` 编译 Go 程序，产物是 `/app` 二进制
2. **最终阶段**：从 `alpine:3.20` 开始，`COPY --from=builder /app /app`，只拿了编译好的二进制

## Step 2：构建

    docker build -t multi-demo 04-multi-stage/

## Step 3：对比镜像大小

    docker images multi-demo
    docker images | grep golang   # 对比编译器镜像大小

最终镜像大概只有 **10MB**，而 Go 编译器镜像是 ~300MB。

## Step 4：验证构建缓存——只构建某个阶段

    docker build --target builder -t multi-builder 04-multi-stage/

这只会执行 builder 阶段的指令，适合调试编译过程。

## Step 5：运行

    docker run --rm -d -p 8004:8000 --name multi-runner multi-demo
    curl http://localhost:8004
    docker rm -f multi-runner

## 检查清单

- [ ] 理解多阶段构建的原理
- [ ] 能用 `COPY --from` 从上一阶段拷贝产物
- [ ] 知道 `--target` 只构建到某个阶段

## 思考题

1. 如果不使用多阶段构建，Go 程序的镜像大概多大？（提示：用 `golang:1.22` 直接跑）
2. 可以在一个 Dockerfile 里定义 3 个或更多阶段吗？什么场景下需要？
3. `COPY --from=xxx` 中的 `xxx` 可以是外部镜像吗？试试 `COPY --from=nginx:alpine /usr/share/nginx/html /static`
4. 多阶段构建能减少多少百分比的安全攻击面？（提示：基础镜像中的工具越少，漏洞越少）
