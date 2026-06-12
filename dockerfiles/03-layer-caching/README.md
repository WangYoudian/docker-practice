
# 练习 3：分层缓存

**目标**：理解 Docker 的镜像分层和缓存机制，写出构建更快的 Dockerfile。

**涉及**：构建缓存原理、指令顺序优化

---

## 背景

Docker 的每一行指令都产生一个新层。构建时，如果某一层的输入（指令 + 文件）没有变化，Docker 会**复用缓存层**，跳过执行。

所以指令的顺序决定了缓存命中率。

## Step 1：好顺序 vs 坏顺序

查看两个 Dockerfile：

    cat 03-layer-caching/Dockerfile       # COPY app.js 在 RUN npm install 之前
    cat 03-layer-caching/Dockerfile.good  # RUN npm install 在 COPY app.js 之前

假设你改了 `app.js`（很频繁），但 `package.json` 没变：

- **坏顺序**：`npm install` 在 `COPY app.js` 之后，改代码会让 `npm install` 的缓存失效，每次都得重装依赖
- **好顺序**：`npm install` 在 `COPY app.js` 之前，只有 `package.json` 变了才重装

## Step 2：验证缓存效果

先构建好的：

    docker build -t cache-good -f 03-layer-caching/Dockerfile.good 03-layer-caching/

第二次构建（不改任何文件）：

    docker build -t cache-good -f 03-layer-caching/Dockerfile.good 03-layer-caching/

观察输出——除了第一行，其他都是 `Using cache`。

> **小提示**：加 `--progress=plain` 让每步输出更清晰，Docker 会显示 `CACHED` 标签，podman 也支持：
> 
>     docker build --progress=plain -t cache-good -f 03-layer-caching/Dockerfile.good 03-layer-caching/
> 
> 输出会逐行标明当前层是否命中缓存，比默认的进度条模式更容易观察。

## Step 3：验证坏顺序的代价

    docker build -t cache-bad -f 03-layer-caching/Dockerfile 03-layer-caching/
    docker build -t cache-bad -f 03-layer-caching/Dockerfile 03-layer-caching/

两次都一样快。现在模拟改代码：

    echo "// change" >> 03-layer-caching/app.js

**好顺序**（只有最后一层失效）：

    docker build -t cache-good -f 03-layer-caching/Dockerfile.good 03-layer-caching/

加上 `--progress=plain` 查看，会看到只有 `COPY app.js` 和之后的层重新执行，`npm install` 标了 `CACHED`。

**坏顺序**（npm install 也跟着重新下载）：
    
    docker build -t cache-bad -f 03-layer-caching/Dockerfile 03-layer-caching/

`npm install` 在 `COPY app.js` 之后，缓存失效，输出中这一步不再是 `CACHED`，而是重新下载所有依赖。

## 运行验证

    docker run --rm -d -p 8003:8000 --name cache-demo cache-good
    curl http://localhost:8003
    docker rm -f cache-demo

## 清理

    git checkout -- 03-layer-caching/app.js  # 还原改过的文件
    docker rmi cache-good cache-bad

## 检查清单

- [ ] 理解"镜像层"和"缓存"的概念
- [ ] 知道为什么 `COPY package.json` 要在 `COPY app.js` 之前
- [ ] 能通过观察构建输出来判断哪些步骤命中了缓存

> **观察技巧**：`--progress=plain` 会逐层标注 `CACHED` 或实际构建用时，是调试缓存行为最直接的方式。

## 思考题

1. 除了指令顺序，还有哪些情况会导致缓存失效？
2. `ADD` 和 `COPY` 在缓存行为上有什么区别？
3. `--no-cache` 参数的作用是什么？何时需要用？
4. `docker build --target` 可以构建多阶段中的某个阶段，它和缓存有什么关系？
