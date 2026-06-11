
IMAGE_NAME ?= docker-practice
IMAGE_TAG ?= latest

default: build

.PHONY: build
build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

.PHONY: test
test:
	docker run --rm $(IMAGE_NAME):$(IMAGE_TAG) python -c "import http.server; print('OK')"

.PHONY: lint
lint:
	docker run --rm -v $(PWD)/Dockerfile:/Dockerfile:ro hadolint/hadolint /Dockerfile

.PHONY: scan
scan:
	trivy image --severity CRITICAL --exit-code 1 $(IMAGE_NAME):$(IMAGE_TAG)

.PHONY: push
push:
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)
	docker push $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)

.PHONY: clean
clean:
	docker rmi $(IMAGE_NAME):$(IMAGE_TAG) 2>/dev/null; true

.PHONY: all
all: build lint test scan
	@echo "All checks passed!"
