
# 练习 7：环境变量

**目标**：掌握通过环境变量向容器注入配置的两种方式。

**涉及命令**：`docker run -e`、`docker run --env-file`

---

## Step 1：通过 -e 传入变量

```bash
docker run --rm -e MY_NAME=Codex alpine sh -c "echo Hello, \$MY_NAME"
# 输出: Hello, Codex
```

也可以传入多个：

```bash
docker run --rm \
  -e DB_HOST=localhost \
  -e DB_PORT=5432 \
  -e DB_USER=admin \
  alpine sh -c "echo Connecting to \$DB_HOST:\$DB_PORT as \$DB_USER"
```

## Step 2：传入宿主机的环境变量

如果省略 `=` 后面的值，Docker 会把宿主机上同名变量的值传进去：

```bash
export HOSTNAME="my-laptop"
docker run --rm -e HOSTNAME alpine sh -c "echo My host is \$HOSTNAME"
```

## Step 3：通过 --env-file 传入

当变量很多时，`-e` 写起来太长。可以用文件：

```bash
cat > /tmp/my-app.env << 'EOF'
APP_ENV=production
APP_DEBUG=false
APP_KEY=base64_abc123
DB_HOST=mysql
DB_PORT=3306
EOF

docker run --rm --env-file /tmp/my-app.env alpine sh -c "echo \$APP_ENV - \$DB_HOST:\$DB_PORT"
```

## Step 4：实际场景 — 跑一个配置了密码的 MySQL

```bash
docker run -d \
  --name my-mysql \
  -e MYSQL_ROOT_PASSWORD=my-secret-pw \
  -e MYSQL_DATABASE=appdb \
  -e MYSQL_USER=appuser \
  -e MYSQL_PASSWORD=apppass \
  mysql:8.0

# 验证：连接进去看看
docker exec -it my-mysql mysql -uappuser -pappdb -e "SHOW DATABASES;"
```

> 实际生产中密码不直接写命令里，会通过 Docker Swarm secrets、Kubernetes secrets 或 .env 文件管理。

## Step 5：查看容器的环境变量

```bash
docker inspect my-mysql --format '{{json .Config.Env}}' | python3 -m json.tool
```

或者进入容器查看：

```bash
docker exec my-mysql env
```

## 清理

```bash
docker rm -f my-mysql
rm /tmp/my-app.env
```

## 检查清单

- [ ] 能用 `-e KEY=VALUE` 传入单个或多个变量
- [ ] 能用 `--env-file` 从文件加载变量
- [ ] 知道 `-e KEY`（不传值）会透传宿主机变量
- [ ] 能用 `docker inspect` 或 `exec env` 查看容器环境变量

## 思考题

1. `--env-file` 如果和 `-e` 同时使用，同一个变量哪个优先级高？
2. 环境变量中如果有敏感信息（如密码），有什么安全风险？你会怎么保护？
3. 除了环境变量，还有哪些向容器注入配置的方式？

---

**🎉 Phase 1 练习全部完成！可以进入 [Phase 2：Dockerfile 实践](../dockerfiles/README.md) 了。**
