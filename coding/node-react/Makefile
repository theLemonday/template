# --- Variables ---
PROJECT ?= react_app
COMPOSE := docker compose

.PHONY: up down logs shell build install lint test clean

up: ## Start dev server with Watch mode
	$(COMPOSE) watch

down: ## Stop containers
	$(COMPOSE) down

logs: ## Follow logs
	$(COMPOSE) logs -f frontend

shell: ## Enter the container shell
	$(COMPOSE) exec frontend /bin/sh

# --- Commands run inside the container ---
install: ## Install new dependencies (e.g., make install PKG=axios)
	$(COMPOSE) exec frontend pnpm add $(PKG)

build: ## Run production build inside container
	$(COMPOSE) exec frontend pnpm run build

lint: ## Run ESLint
	$(COMPOSE) exec frontend pnpm run lint

test: ## Run tests (Vitest)
	$(COMPOSE) exec frontend pnpm run test

clean: ## Clean up Docker artifacts
	$(COMPOSE) down -v --remove-orphans
