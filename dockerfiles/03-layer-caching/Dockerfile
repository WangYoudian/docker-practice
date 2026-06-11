
# 坏顺序：源码先拷贝，依赖后安装
FROM node:18-slim
WORKDIR /app
COPY package.json .
COPY app.js .
RUN npm install
EXPOSE 8000
CMD ["node", "app.js"]
