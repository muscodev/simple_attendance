# Makefile for FastAPI Attendance App

# Variables
PYTHON = uv run python
UV_ENV = uv run
PYTEST = uv run pytest
PIP = uv pip
FLAKE8 = uv run flake8
BLACK = uv run black
ISORT = uv run isort

# Default target
.DEFAULT_GOAL := help

# Help target
help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST)| sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m => %s\n", $$1, $$2}'

# Check system requirements
check-deps: ## Check if required tools are installed
	@echo "🔍 Checking system requirements..."
	@command -v uv >/dev/null 2>&1 || { echo "❌ UV not found"; exit 1; }
	@command -v node >/dev/null 2>&1 || { echo "❌ Node.js not found"; exit 1;}
	@command -v npm >/dev/null 2>&1 || { echo "❌ npm not found"; exit 1; }
	@echo "✅ All required tools are installed!"
	@echo "📋 Versions:"
	@echo "   UV: $$(uv --version)"
	@echo "   Node: $$(node --version)"
	@echo "   npm: $$(npm --version)"


# Development setup
install-api: ## Install API dependencies
	@echo "📋 Installing API dependencies..."
	uv sync --dev



install-web: ## Install web dependencies
	@echo "📋 Installing web dependencies..."
	cd web && npm install

install-api-prod: ## install API dependencies for production
	uv sync

install: check-deps install-api install-web ## Install all dependencies
	@echo "✅ All dependencies installed successfully!"

install-prod: check-deps install-api-prod install-web ## Install all dependencies
	@echo "✅ All dependencies installed successfully!"


# Code quality
lint: ## Run flake8 linting
	$(FLAKE8) .


format: ## Format code with black and isort
	$(ISORT) .
	$(BLACK) .

format-check: ## Check if code is formatted correctly
	$(BLACK) --check .
	$(ISORT) --check-only .

# FastAPI server
api-run-dev: ## Run the API server in development
	$(UV_ENV) fastapi dev api/main.py

api-run-prod: ## Run the API server in production mode
	$(UV_ENV) fastapi run api/main.py

web-dev: ## Run the web server in development
	cd web && npm run dev

web-build: ## Build the web application
	cd web && npm run build

web-preview: ## Preview the built web application
	cd web && npm run preview
	
# Database (adjust based on your needs)
migrate: ## Run database migrations
	$(UV_ENV)  alembic upgrade head

# Quality checks (combine multiple checks)
check: lint format-check


# Testing
test: ## Run tests
	PYTHONPATH=. $(PYTEST) tests/ $(filter-out $@,$(MAKECMDGOALS))	

test-cov: ## Run tests with coverage
	PYTHONPATH=. $(PYTEST) --cov=api --cov-report=html  --cov-report=xml

# Clean up
clean: ## Clean up cache and temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf .coverage

# Build (if you need to build packages)
build: clean ## Build the package
	uv build

.PHONY: help install install-prod lint format format-check test test-cov test-fast dev migrate check clean build