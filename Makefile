.PHONY: install dev build test lint format migrate seed logs down clean compose-check

COMPOSE := $(shell if command -v docker-compose >/dev/null 2>&1; then echo docker-compose; elif docker compose version >/dev/null 2>&1; then echo "docker compose"; fi)

compose-check:
	@if [ -z "$(COMPOSE)" ]; then \
		echo "✗ Docker Compose not found. Install docker-compose or Docker CLI compose plugin."; \
		exit 127; \
	fi

install: ## Install all dependencies
	@echo "→ Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "→ Installing frontend dependencies..."
	cd frontend && npm install

dev: compose-check ## Start all services in development mode
	@echo "→ Starting StudyAI in development mode..."
	$(COMPOSE) up --build

build: compose-check ## Build production Docker images
	@echo "→ Building production images..."
	$(COMPOSE) -f docker-compose.yml build

test: ## Run all tests
	@echo "→ Running backend tests..."
	cd backend && pytest tests/ -v --asyncio-mode=auto
	@echo "→ Running frontend type check..."
	cd frontend && npx tsc --noEmit

lint: ## Lint all code
	@echo "→ Linting Python..."
	cd backend && ruff check .
	@echo "→ Linting TypeScript..."
	cd frontend && npx eslint src/

format: ## Format all code
	@echo "→ Formatting Python..."
	cd backend && ruff format .
	@echo "→ Formatting TypeScript..."
	cd frontend && npx prettier --write src/

migrate: ## Run Supabase migrations
	@echo "→ Running database migrations..."
	supabase db push

seed: ## Seed demo data
	@echo "→ Seeding demo data..."
	cd backend && python ../scripts/seed_demo.py

logs: compose-check ## Tail all service logs
	$(COMPOSE) logs -f

down: compose-check ## Stop all services
	$(COMPOSE) down

clean: compose-check ## Remove all containers, volumes, and build artifacts
	$(COMPOSE) down -v --remove-orphans
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name node_modules -exec rm -rf {} +
	find . -name "*.pyc" -delete
