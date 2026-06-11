
# 练习 1：第一个 Dockerfile

**目标**：从一个简单的 Python HTTP 服务开始，理解 Dockerfile 的基本指令和构建流程。

**涉及指令**：`FROM`、`WORKDIR`、`COPY`、`EXPOSE`、`CMD`

---

## Step 1：查看文件

```bash
ls -la
# Dockerfile   app.py
```

`app.py` 是一个极简的 HTTP 服务器，监听 8000 端口，返回 "Hello from Docker!"。

## Step 2：构建镜像

```bash
docker build -t hello-app .
```

- `-t hello-app` 给镜像打标签
- `.` 是构建上下文路径（当前目录会被发给 Docker daemon）

## Step 3：查看构建过程

输出类似：
```
Step 1/5 : FROM python:3.11-slim
 ---> abc123
Step 2/5 : WORKDIR /app
 ---> ...
```

每一步对应 Dockerfile 的一条指令，每一步都会产生一个新镜像层。

## Step 4：运行容器

```bash
docker run -d -p 8000:8000 --name hello hello-app
curl http://localhost:8000
# 输出: Hello from Docker!
```

## Step 5：理解每条指令

| 指令 | 作用 |
|------|------|
| `FROM` | 指定基础镜像（所有 Dockerfile 的第一条指令）|
| `WORKDIR` | 设置工作目录（后续指令的相对路径基于此）|
| `COPY` | 从构建上下文复制文件到镜像 |
| `EXPOSE` | 声明容器运行时监听的端口（文档性，不映射）|
| `CMD` | 容器启动时的默认命令 |

## 延伸：用环境变量传名字

```bash
docker run -d -p 8001:8000 -e NAME=World hello-app
curl http://localhost:8001
# 输出: Hello from World!
```

## 清理

```bash
docker rm -f hello
```

## 检查清单

- [ ] 能写出一个完整的 Dockerfile
- [ ] 理解 `docker build -t` 的用法
- [ ] 知道每条指令的作用
- [ ] 能运行容器并访问服务

## 思考题

1. 如果构建时不用 `-t` 会怎样？怎么运行没有标签的镜像？
2. `EXPOSE 8000` 之后还需要 `-p 8000:8000` 吗？试试不加 `-p` 能否访问。
3. 如果把 `CMD ["python", "app.py"]` 改成 `CMD python app.py`（shell 格式），有什么区别？
