
# 练习 2：构建上下文与 .dockerignore

**目标**：理解构建上下文的概念，学会用 `.dockerignore` 减小上下文体积。

**涉及**：`COPY` 指令、`.dockerignore` 文件

---

## Step 1：演示问题——拷贝了不需要的文件

先回到 dockerfiles 目录，然后构建：

    cd ..
    docker build -t build-context-bad -f 02-build-context/Dockerfile 02-build-context/

> 注意 `docker build` 最后的参数是上下文路径，而不是 Dockerfile 路径。

## Step 2：查看构建上下文的大小

    docker build -t build-context -f 02-build-context/Dockerfile 02-build-context/

看输出第一行：`Sending build context to Docker daemon  XX.XXkB`

现在创建一个大文件模拟"不该存在的东西"：

    dd if=/dev/zero of=02-build-context/bigfile.bin bs=1M count=1 2>/dev/null
    docker build -t build-context-big -f 02-build-context/Dockerfile 02-build-context/

可以看到发送到 daemon 的上下文变大了不少。清理大文件：

    rm 02-build-context/bigfile.bin

## Step 3：.dockerignore 的作用

检查已有的 `.dockerignore`：

    cat 02-build-context/.dockerignore

这个文件告诉 Docker 构建时忽略哪些模式的文件。即使你忘记删大文件，只要把它的模式加到 `.dockerignore` 里，它就不会被发送到 daemon。

## Step 4：构建并运行

    docker build -t build-context -f 02-build-context/Dockerfile 02-build-context/
    docker run --rm -d -p 8002:8000 --name ctx-demo build-context
    curl http://localhost:8002
    docker rm -f ctx-demo

## 检查清单

- [ ] 理解"构建上下文"的概念
- [ ] 知道 `.dockerignore` 的语法和用途
- [ ] 知道 `-f` 参数可以指定 Dockerfile 路径

## 思考题

1. `COPY . .` 会把 `.dockerignore` 里的文件也拷贝进去吗？
2. 如果 Dockerfile 在子目录中，而你想把项目根目录作为上下文，怎么写 `docker build` 命令？
3. 构建上下文中有一个 500MB 的压缩包，但它并不被 COPY，会影响构建速度吗？为什么？
