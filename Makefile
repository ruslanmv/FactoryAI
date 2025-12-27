.PHONY: help install install-dev sync clean lint format test test-cov validate run-app run-feature run-debug status info build check-uv
.DEFAULT_GOAL := help

# ANSI color codes
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# Python and uv settings
PYTHON := python3
UV := uv
PACKAGE_NAME := factoryai

help: ## Show this help message
	@echo "$(BLUE)FactoryAI Suite - Makefile Commands$(NC)"
	@echo "$(BLUE)=====================================$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Quick Start:$(NC)"
	@echo "  1. make install      # Install FactoryAI"
	@echo "  2. make sync         # Sync submodules"
	@echo "  3. make validate     # Validate installation"
	@echo "  4. make status       # Check component status"
	@echo ""

check-uv: ## Check if uv is installed
	@command -v $(UV) >/dev/null 2>&1 || { \
		echo "$(RED)Error: 'uv' is not installed.$(NC)"; \
		echo "$(YELLOW)Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh$(NC)"; \
		echo "$(YELLOW)Or visit: https://github.com/astral-sh/uv$(NC)"; \
		exit 1; \
	}
	@echo "$(GREEN)✓ uv is installed$(NC)"

install: check-uv ## Install FactoryAI package (production)
	@echo "$(BLUE)Installing FactoryAI...$(NC)"
	$(UV) pip install -e .
	@echo "$(GREEN)✓ Installation complete$(NC)"

install-dev: check-uv ## Install FactoryAI with development dependencies
	@echo "$(BLUE)Installing FactoryAI with development dependencies...$(NC)"
	$(UV) pip install -e ".[dev]"
	@echo "$(GREEN)✓ Development installation complete$(NC)"

sync: ## Synchronize all git submodules
	@echo "$(BLUE)Synchronizing submodules...$(NC)"
	@chmod +x sync.sh
	@./sync.sh
	@echo "$(GREEN)✓ Submodules synchronized$(NC)"

clean: ## Clean build artifacts and caches
	@echo "$(BLUE)Cleaning build artifacts...$(NC)"
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info
	@rm -rf .eggs/
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name '*.pyc' -delete
	@find . -type f -name '*.pyo' -delete
	@find . -type f -name '*~' -delete
	@rm -rf .pytest_cache/
	@rm -rf .mypy_cache/
	@rm -rf .ruff_cache/
	@rm -rf htmlcov/
	@rm -rf .coverage
	@rm -rf coverage.xml
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

lint: ## Run code linters (ruff + mypy)
	@echo "$(BLUE)Running linters...$(NC)"
	@echo "$(YELLOW)Running ruff...$(NC)"
	@$(UV) run ruff check $(PACKAGE_NAME)/ tests/ || true
	@echo "$(YELLOW)Running mypy...$(NC)"
	@$(UV) run mypy $(PACKAGE_NAME)/ || true
	@echo "$(GREEN)✓ Linting complete$(NC)"

format: ## Format code with black and isort
	@echo "$(BLUE)Formatting code...$(NC)"
	@echo "$(YELLOW)Running black...$(NC)"
	@$(UV) run black $(PACKAGE_NAME)/ tests/
	@echo "$(YELLOW)Running isort...$(NC)"
	@$(UV) run isort $(PACKAGE_NAME)/ tests/
	@echo "$(YELLOW)Running ruff fix...$(NC)"
	@$(UV) run ruff check --fix $(PACKAGE_NAME)/ tests/ || true
	@echo "$(GREEN)✓ Formatting complete$(NC)"

test: ## Run tests
	@echo "$(BLUE)Running tests...$(NC)"
	@$(UV) run pytest tests/ -v
	@echo "$(GREEN)✓ Tests complete$(NC)"

test-cov: ## Run tests with coverage report
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	@$(UV) run pytest tests/ -v --cov=$(PACKAGE_NAME) --cov-report=term-missing --cov-report=html
	@echo "$(GREEN)✓ Coverage report generated$(NC)"
	@echo "$(YELLOW)View HTML report: htmlcov/index.html$(NC)"

validate: ## Validate FactoryAI installation
	@echo "$(BLUE)Validating installation...$(NC)"
	@$(PYTHON) -m $(PACKAGE_NAME).cli validate

status: ## Show status of all components
	@$(PYTHON) -m $(PACKAGE_NAME).cli status

info: ## Show FactoryAI information
	@$(PYTHON) -m $(PACKAGE_NAME).cli info

list: ## List all available components
	@$(PYTHON) -m $(PACKAGE_NAME).cli list

run-app: ## Run Factory-App-AI component
	@echo "$(BLUE)Starting Factory-App-AI...$(NC)"
	@$(PYTHON) -m $(PACKAGE_NAME).cli run app

run-feature: ## Run Factory-Feature component
	@echo "$(BLUE)Starting Factory-Feature...$(NC)"
	@$(PYTHON) -m $(PACKAGE_NAME).cli run feature

run-debug: ## Run Factory-Debug component (Coming Soon)
	@echo "$(BLUE)Starting Factory-Debug...$(NC)"
	@$(PYTHON) -m $(PACKAGE_NAME).cli run debug

build: clean ## Build distribution packages
	@echo "$(BLUE)Building distribution packages...$(NC)"
	@$(UV) build
	@echo "$(GREEN)✓ Build complete$(NC)"
	@ls -lh dist/

pre-commit: format lint test ## Run pre-commit checks (format, lint, test)
	@echo "$(GREEN)✓ All pre-commit checks passed$(NC)"

check: lint test ## Run all checks (lint + test)
	@echo "$(GREEN)✓ All checks passed$(NC)"

# Development workflow targets
dev-setup: install-dev sync ## Complete development setup
	@echo "$(GREEN)✓ Development environment ready$(NC)"
	@echo "$(YELLOW)Run 'make validate' to check installation$(NC)"

# CI/CD targets
ci: check-uv lint test ## CI pipeline (lint + test)
	@echo "$(GREEN)✓ CI checks passed$(NC)"

# Documentation targets
docs-serve: ## Serve documentation locally (requires sphinx)
	@echo "$(BLUE)Serving documentation...$(NC)"
	@cd docs && $(UV) run sphinx-autobuild . _build/html

docs-build: ## Build documentation (requires sphinx)
	@echo "$(BLUE)Building documentation...$(NC)"
	@cd docs && $(UV) run sphinx-build -b html . _build/html
	@echo "$(GREEN)✓ Documentation built$(NC)"

# Upgrade targets
upgrade-deps: check-uv ## Upgrade all dependencies
	@echo "$(BLUE)Upgrading dependencies...$(NC)"
	@$(UV) pip install --upgrade -e ".[dev]"
	@echo "$(GREEN)✓ Dependencies upgraded$(NC)"

# Version management
version: ## Show current version
	@$(PYTHON) -c "from factoryai import __version__; print(f'FactoryAI version: {__version__}')"

# Complete workflow
all: clean install-dev sync validate check ## Complete setup and validation workflow
	@echo "$(GREEN)✓ Complete workflow finished$(NC)"
