
# 练习 5：数据持久化

**目标**：理解容器生命周期和数据持久化的关系，掌握 volume 和 bind mount 两种方式。

**涉及命令**：`docker run -v`、`docker volume`

---

## 背景知识

容器删除后，内部所有数据都会消失。如果希望数据保留，需要用两种方式：

- **Volume**：由 Docker 管理，存在特定目录（Linux: `/var/lib/docker/volumes/`）
- **Bind mount**：把宿主机任意目录挂载进容器

## Step 1：演示数据丢失（反面教材）

```bash
# 创建一个写文件的容器
docker run --name data-test alpine touch /tmp/hello.txt

# 删除容器
docker rm data-test

# 重新创建一个同名容器，文件不在了
docker run --name data-test alpine ls /tmp/hello.txt
# ls: /tmp/hello.txt: No such file or directory

docker rm data-test
```

## Step 2：使用 Volume 持久化数据

```bash
# 创建一个 volume
docker volume create my-data

# 查看 volume
docker volume ls
docker volume inspect my-data
# 可以看到 Mountpoint，那就是宿主机上的真实路径
```

用这个 volume 跑一个容器：

```bash
docker run -d --name db -v my-data:/var/lib/mysql mysql:8.0
```

> 注意：`-v volume-name:/container/path`，volume 名称在前，容器路径在后。

现在即使删除容器，volume 里的数据还在：

```bash
docker rm -f db
docker volume ls          # my-data 还在
docker volume rm my-data  # 手动删掉 volume
```

## Step 3：匿名 Volume

```bash
# 不指定 volume 名称，Docker 自动生成一个随机名字
docker run -d --name blog -v /var/lib/data alpine sleep 300
docker volume ls
# 可以看到一个长 hash 的 volume
docker rm -f blog
docker volume prune       # 清理无主的匿名 volume
```

## Step 4：Bind Mount（直接挂载宿主机目录）

创建一个本地文件作为示例：

```bash
mkdir -p /tmp/docker-bind
echo "Hello from host!" > /tmp/docker-bind/hi.txt
```

挂载到容器内：

```bash
docker run --rm -v /tmp/docker-bind:/mnt alpine cat /mnt/hi.txt
# 输出: Hello from host!
```

**双向同步**——在容器内修改，宿主机会看到：

```bash
docker run --rm -v /tmp/docker-bind:/mnt alpine sh -c "echo 'Modified in container' > /mnt/hi.txt"
cat /tmp/docker-bind/hi.txt
# 输出: Modified in container
```

**应用场景**：开发时挂载代码目录，改完代码容器内立即生效（热重载）：

```bash
docker run -d --name dev -v $(pwd):/app -p 3000:3000 node:18
# 宿主机改代码，容器里 /app 同步更新
```

## Step 5：只读挂载

```bash
docker run --rm -v /tmp/docker-bind:/mnt:ro alpine sh -c "echo 'write' > /mnt/test.txt"
# 会报错：Read-only file system
```

## 清理

```bash
docker rm -f db dev 2>/dev/null
docker volume rm my-data 2>/dev/null
docker volume prune -f
rm -rf /tmp/docker-bind
```

## 检查清单

- [ ] 理解容器删除后数据丢失的原因
- [ ] 能用 `docker volume create` 创建独立 volume
- [ ] 能用 `-v` 将 volume 挂载到容器
- [ ] 能用 `-v` 做 bind mount，理解双向同步
- [ ] 知道 `:ro` 只读挂载

## 思考题

1. Volume 和 Bind Mount 在实际使用中分别适合什么场景？
2. 如果你在容器外修改了 bind mount 里的文件，容器内多久能看到变化？
3. 两个容器可以共享同一个 volume 吗？怎么验证？
4. `--mount` 是 `-v` 的新替代语法，查一下 `--mount type=bind,src=...,dst=...` 怎么写，和 `-v` 有什么优势？
