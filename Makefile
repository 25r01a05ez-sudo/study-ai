.PHONY: install dev build test lint format migrate seed logs down clean

install: ## Install all dependencies
	@echo "→ Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "→ Installing frontend dependencies..."
	cd frontend && npm install

dev: ## Start all services in development mode
	@echo "→ Starting StudyAI in development mode..."
	docker-compose up --build

build: ## Build production Docker images
	@echo "→ Building production images..."
	docker-compose -f docker-compose.yml build

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

logs: ## Tail all service logs
	docker-compose logs -f

down: ## Stop all services
	docker-compose down

clean: ## Remove all containers, volumes, and build artifacts
	docker-compose down -v --remove-orphans
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name node_modules -exec rm -rf {} +
	find . -name "*.pyc" -delete
