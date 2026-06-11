
# ===== Stage 1: Build =====
FROM golang:1.22-alpine AS builder
WORKDIR /src
COPY main.go .
RUN CGO_ENABLED=0 go build -o /app main.go

# ===== Stage 2: Run =====
FROM alpine:3.20
RUN adduser -D appuser
COPY --from=builder /app /app
USER appuser
EXPOSE 8000
CMD ["/app"]
