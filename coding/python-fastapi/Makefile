# --- Variables ---
PROJECT ?= fastapi_base
COMPOSE := docker compose
# You can set this via command line: make build-prod IMAGE_REGISTRY=myreg.com/
IMAGE_REGISTRY ?=

.PHONY: up down logs shell lint test clean build-prod

up: ## Start dev environment
	$(COMPOSE) watch

down: ## Stop containers
	$(COMPOSE) down

logs: ## Follow backend logs
	$(COMPOSE) logs -f backend

shell: ## Enter backend shell
	$(COMPOSE) exec backend /bin/bash

lint: ## Run Ruff (Linter & Formatter)
	$(COMPOSE) exec backend ruff check .
	$(COMPOSE) exec backend ruff format .

test: ## Run Pytest
	$(COMPOSE) exec backend pytest

build-prod: ## Build Production Image
	docker build \
		--target prod \
		--build-arg IMAGE_REGISTRY=$(IMAGE_REGISTRY) \
		-t $(PROJECT):latest .

clean: ## Remove artifacts
	$(COMPOSE) down -v
	rm -rf .venv __pycache__ .ruff_cache .pytest_cache
