# --- Variables ---
PROJECT ?= django_app
COMPOSE := docker compose

.PHONY: up down logs migrate migrations superuser shell test

up: ## Start the dev environment with Watch mode
	$(COMPOSE) watch

down: ## Stop containers
	$(COMPOSE) down

logs: ## Follow logs
	$(COMPOSE) logs -f backend

# --- Django Commands (Run inside container) ---
migrate: ## Apply DB migrations
	$(COMPOSE) exec backend python manage.py migrate

migrations: ## Make new migrations
	$(COMPOSE) exec backend python manage.py makemigrations

superuser: ## Create a superuser
	$(COMPOSE) exec backend python manage.py createsuperuser

shell: ## Enter the Django shell
	$(COMPOSE) exec backend python manage.py shell

test: ## Run tests (pytest recommended)
	$(COMPOSE) exec backend pytest
