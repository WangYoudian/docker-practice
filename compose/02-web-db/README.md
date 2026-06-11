
# 练习 2：Web + PostgreSQL

**目标**：用 Compose 编排应用 + 数据库，掌握初始化脚本和数据持久化。

**涉及**：PostgreSQL 镜像、init 脚本、named volume

---

## Step 1：查看 compose.yml

    cat 02-web-db/compose.yml

注意 db 服务挂载了两个 volume：
- `pg-data:/var/lib/postgresql/data` — 持久化数据库文件
- `./db/init.sql:/docker-entrypoint-initdb.d/init.sql` — 初始化脚本

PostgreSQL 镜像会自动执行 `docker-entrypoint-initdb.d/` 下的 `.sql` 文件。

## Step 2：启动

    cd 02-web-db
    docker compose up -d

db 服务启动较慢，等待几十秒完成初始化。

    docker compose logs -f db
    # 看到 "database system is ready to accept connections" 即可

## Step 3：测试

    curl http://localhost:8102
    # 输出: Visit #0 at ...

    curl http://localhost:8102
    # 输出: Visit #1 at ...

## Step 4：验证数据持久化

    docker compose down     # 停止，但不删 volume
    docker compose up -d    # 重新启动
    curl http://localhost:8102
    # 数据应该还在，计数继续

    docker compose down -v  # 这次删除 volume
    docker compose up -d
    curl http://localhost:8102
    # 数据从头开始

## 清理

    docker compose down -v
    cd ..

## 检查清单

- [ ] 理解 `docker-entrypoint-initdb.d/` 初始化机制
- [ ] 知道 named volume 和 bind mount 在 Compose 中的写法
- [ ] 理解 `docker compose down` 和 `-v` 的区别

## 思考题

1. 如果 PostgreSQL 容器已经初始化完了，再更新 `init.sql` 会生效吗？如何重新初始化？
2. 生产环境中 DB 密码直接写在 `compose.yml` 里的安全隐患是什么？有什么替代方案？
3. `postgres:16-alpine` 的 `16` 和 `alpine` 分别指什么？
4. 如果 app 在 db 完全就绪之前就启动连接，会发生什么？下一节会解决这个问题。
