
# 练习 4：多环境 Compose

**目标**：掌握多文件 Compose 的合并机制，分别配置开发和生产环境。

**涉及**：`compose.override.yml`、多文件 `-f`、Compose 合并规则

---

## 背景

Compose 支持加载多个 yml 文件，自动合并。这是一个非常实用的模式：

| 环境 | 命令 | 加载的文件 |
|------|------|-----------|
| 开发 | `docker compose up` | `compose.yml` + `compose.override.yml`（自动）|
| 生产 | `docker compose -f compose.yml -f compose.prod.yml up` | 手动指定 |
| 测试 | `docker compose -f compose.yml -f compose.test.yml up` | 手动指定 |

## Step 1：查看各文件

    cat 04-multi-env/compose.yml           # 基础定义
    cat 04-multi-env/compose.override.yml  # 开发环境 overribe
    cat 04-multi-env/compose.prod.yml      # 生产环境配置

**compose.override.yml** 是 Compose 的默认 overribe 文件。执行 `docker compose up` 时，它会被自动加载（无需 `-f`）。

## Step 2：以开发模式启动

    cd 04-multi-env
    docker compose up -d
    curl http://localhost:8104
    # 输出: [development] Host: ...

开发模式下，`./app` 目录被 bind mount 到容器内，修改代码立即生效。

## Step 3：修改代码验证热加载

    echo 'print("hot reload test")' >> app/app.py
    curl http://localhost:8104
    # 能看到新加的 print 在日志里（但 HTTP 响应不变，因为 Python 不会自动重载）
    # 对于支持热重载的框架（Node.js nodemon、Flask debug 模式），改完代码立刻生效

恢复文件：
    git checkout -- app/app.py

## Step 4：以生产模式启动

    docker compose down
    docker compose -f compose.yml -f compose.prod.yml up -d
    curl http://localhost:8104
    # 输出: [production] Host: ...

生产模式有资源限制、自动重启和健康检查。

## Step 5：验证 service 的健康状态

    docker compose ps
    # STATUS 列应该显示 (healthy)

## 清理

    docker compose down
    cd ..

## 检查清单

- [ ] 理解 `compose.override.yml` 的自动加载机制
- [ ] 理解多文件 `-f` 的合并规则（同名 key 覆盖）
- [ ] 能配置开发和生产两种环境
- [ ] 知道 `restart: always` 和资源限制的写法

## 思考题

1. Compose 合并多个 yml 文件时，对 list 类型（如 ports、volumes）是替换还是追加？
2. 除了 `compose.override.yml`，还有其他命名约定吗？（如 `.env` 文件的作用）
3. 生产环境中，`build: ./app` 适合吗？在生产中一般用什么替代？
4. `deploy.resources.limits` 和 `docker run --memory` 的关系是什么？
5. docker compose config 命令有什么用？试试 `docker compose -f compose.yml -f compose.prod.yml config`
