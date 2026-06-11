
FROM python:3.11-slim
WORKDIR /app
COPY app.py .
HEALTHCHECK --interval=5s --timeout=3s --retries=2 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1
EXPOSE 8000
CMD ["python", "app.py"]
