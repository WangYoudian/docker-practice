
FROM python:3.11-slim

# 创建非 root 用户
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app
COPY app.py .

# 切换到非 root 用户
USER appuser

EXPOSE 8000
CMD ["python", "app.py"]
