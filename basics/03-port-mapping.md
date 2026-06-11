
# 练习 3：端口映射

**目标**：理解容器端口与宿主机端口的映射关系，能同时运行多个容器。

**涉及命令**：`docker run -d -p`、`docker port`

---

## Step 1：将容器端口映射到宿主机

```bash
docker run -d --name web -p 8080:80 nginx:alpine
```

参数 `-p 8080:80` 含义：
> `-p <宿主机端口>:<容器端口>`

意思是宿主机的 `8080` 端口收到的流量，转发到容器的 `80` 端口。

**验证**：
```bash
curl http://localhost:8080
# 或者打开浏览器访问 http://localhost:8080
```

应该能看到 Nginx 的默认页面。

## Step 2：查看端口映射关系

```bash
docker port web
# 输出: 80/tcp -> 0.0.0.0:8080

docker inspect web | grep -i port
```

## Step 3：映射到随机宿主机端口

如果不想指定宿主机端口，让 Docker 自动分配：

```bash
docker run -d --name web-random -p 80 nginx:alpine
docker port web-random
# 输出: 80/tcp -> 0.0.0.0:32768  (端口是随机的)
```

## Step 4：同时运行多个 Nginx（不同端口）

```bash
docker run -d --name web1 -p 8081:80 nginx:alpine
docker run -d --name web2 -p 8082:80 nginx:alpine

# 验证
curl -s http://localhost:8081 | head -1
curl -s http://localhost:8082 | head -1
```

两个独立的容器，互不干扰。

## Step 5：映射到特定 IP 地址

```bash
docker run -d --name web-local -p 127.0.0.1:8083:80 nginx:alpine
```

此时只能从本机访问 `localhost:8083`，局域网其他机器无法访问（安全性）。

## 清理

```bash
docker rm -f web web-random web1 web2 web-local
```

## 检查清单

- [ ] 理解 `-p host:container` 的语义
- [ ] 能用 `docker port` 查看映射关系
- [ ] 能同时运行多个容器用不同端口
- [ ] 知道如何把容器端口绑定到指定 IP

## 思考题

1. 如果宿主机 8080 端口已被占用，再 `-p 8080:80` 会怎样？
2. 容器内的进程监听的是哪个端口？能看到宿主机端口吗？
3. 如果 Docker 容器是 `--network host` 模式，`-p` 参数还生效吗？
