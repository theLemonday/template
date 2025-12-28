REGISTRY?= docker.io

VERSION ?= $(shell git rev-parse --short HEAD)

# Expect input like PROJECT=app/module
PROJECT ?= unknown/unknown

# If we have PROJECT=app/module
# Then APP_NAME=app
# MODULE_NAME = module
APP_NAME := $(word 1, $(subst /, ,$(PROJECT)))
MODULE_NAME := $(word 2, $(subst /, ,$(PROJECT)))

IMAGE_TAG := $(REGISTRY)/$(APP_NAME)/$(MODULE_NAME)

.PHONY: help info build-dev test build-prod push release verify-input install-pre-commit

help: ## Show this help message
	@echo "Usage: make [target] PROJECT={app}/{module}"
	@echo "Example: make release PROJECT=ecommerce/cart"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

verify-input:
	@if [ "$(PROJECT)" = "unknown/unknown" ]; then \
		echo "\033[31mError: PROJECT variable is required. Format: app/module\033[0m"; \
		exit 1; \
	fi

info: verify-input ## Print parsed configuration
	@echo "------------------------------------"
	@echo "App:      $(APP_NAME)"
	@echo "Module:   $(MODULE_NAME)"
	@echo "Registry: $(REGISTRY)"
	@echo "Version:  $(VERSION)"
	@echo "Image:    $(IMAGE_TAG)"
	@echo "------------------------------------"

build-dev: verify-input ## Build the Development stage (includes deps)
	@echo "Building Dev image for $(MODULE_NAME)..."
	docker build \
		--target dev \
		--build-arg IMAGE_REGISTRY=$(REGISTRY)/ \
		-t $(IMAGE_TAG):dev .

test: build-dev ## Run tests inside the Dev container
	@echo "Running tests..."
	# We run the test command inside the isolated dev container
	docker run --rm $(IMAGE_TAG):dev pnpm test

build-prod: verify-input ## Build the Production stage (Optimized)
	@echo "Building Prod image..."
	docker build \
		--target prod \
		--build-arg IMAGE_REGISTRY=$(REGISTRY)/ \
		-t $(IMAGE_TAG):$(VERSION) \
		-t $(IMAGE_TAG):latest .

push: ## Push Prod images to registry
	@echo "Pushing images to $(REGISTRY)..."
	docker push $(IMAGE_TAG):$(VERSION)
	docker push $(IMAGE_TAG):latest

release: test build-prod push ## Run full release pipeline
	@echo "\nSuccessfully transformed $(PROJECT) from Dev to Prod!"

install-pre-commit: ## Install pre-commit hooks
	@echo "\nInstalling pre-commit hooks"
	pre-commit install
