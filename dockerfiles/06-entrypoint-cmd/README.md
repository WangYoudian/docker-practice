
# 练习 6：ENTRYPOINT vs CMD

**目标**：彻底理解 `ENTRYPOINT` 和 `CMD` 各自的角色以及组合方式。

**涉及**：`ENTRYPOINT`、`CMD`、JSON 格式 vs shell 格式

---

## 规则速查

| 组合 | 效果 |
|------|------|
| 只有 CMD | `CMD echo hi` — 容器运行这个命令，`docker run ... ls` 可覆盖 |
| 只有 ENTRYPOINT | `ENTRYPOINT echo hi` — 执行该命令，`docker run ... xxx` 会追加为参数 |
| ENTRYPOINT + CMD | `ENTRYPOINT ["echo"]` + `CMD ["hi"]` — 组合为 `echo hi`，且 `docker run ... hello` 会变成 `echo hello` |

## Step 1：构建

    docker build -t greet 06-entrypoint-cmd/

## Step 2：默认行为

    docker run greet
    # 输出: Hello Docker

`ENTRYPOINT` = `["echo", "Hello"]`，`CMD` = `["Docker"]`，组合为 `echo Hello Docker`。

## Step 3：覆盖 CMD（传参）

    docker run greet World
    # 输出: Hello World

`CMD` 被 `World` 覆盖，最终执行：`echo Hello World`

## Step 4：覆盖 ENTRYPOINT

    docker run --entrypoint sh greet -c "echo Hi from shell"
    # 输出: Hi from shell

`--entrypoint` 完全替换了 `ENTRYPOINT`。

## Step 5：JSON 格式 vs Shell 格式

    # JSON 格式（推荐）——没有 shell 包装
    ENTRYPOINT ["echo", "Hello"]
    CMD ["Docker"]
    # 最终: echo Hello Docker

    # Shell 格式——有 shell 包装
    ENTRYPOINT echo Hello
    # 最终: /bin/sh -c "echo Hello"
    # 注意: CMD 在 shell 格式 ENTRYPOINT 下不会被当作参数传递！

## 典型实践

```dockerfile
# 固定入口，允许传参
ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]
```

```dockerfile
# 工具类镜像，默认执行某项操作，允许覆盖
ENTRYPOINT ["aws-cli"]
CMD ["--help"]
```

```dockerfile
# 纯 CMD，允许完全替换
CMD ["python", "app.py"]
```

## 检查清单

- [ ] 理解 `ENTRYPOINT` + `CMD` 的组合规则
- [ ] 知道 JSON 格式和 shell 格式的区别
- [ ] 知道 `docker run --entrypoint` 的用法

## 思考题

1. 如果一个 Dockerfile 同时有 `ENTRYPOINT` 和 `CMD`，且都是 shell 格式，会发生什么？
2. 你写了一个 MySQL 镜像，`ENTRYPOINT ["docker-entrypoint.sh"]`，用户想用 `docker run ... --help` 而不是启动 MySQL 怎么办？
3. 写一个 Dockerfile，让 `docker run mytool` 执行默认操作，但 `docker run mytool backup` 执行备份命令。
