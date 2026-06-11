
# 多架构示例
FROM --platform=$TARGETPLATFORM alpine:3.20
ARG TARGETPLATFORM
ARG BUILDPLATFORM
RUN echo "Build on: $BUILDPLATFORM, Target: $TARGETPLATFORM"
CMD echo "Hello from $(uname -m)"
