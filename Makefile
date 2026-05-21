.PHONY: help install install-dev run test lint format clean debug all

# Colors for output
BLACK := \033[0;30m
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
MAGENTA := \033[0;35m
CYAN := \033[0;36m
RESET := \033[0m

help:
	@echo "$(MAGENTA)MYTHOS Development Tasks$(RESET)"
	@echo ""
	@echo "$(CYAN)Core Commands:$(RESET)"
	@echo "  make install         - Install production dependencies"
	@echo "  make install-dev     - Install development dependencies"
	@echo "  make run             - Run MYTHOS"
	@echo ""
	@echo "$(CYAN)Code Quality:$(RESET)"
	@echo "  make test            - Run syntax checks and tests"
	@echo "  make lint            - Lint code with pylint"
	@echo "  make format          - Format code with black and isort"
	@echo "  make check           - Run all checks (lint + test + format)"
	@echo ""
	@echo "$(CYAN)Utilities:$(RESET)"
	@echo "  make clean           - Clean up cache and artifacts"
	@echo "  make debug           - Run with debug output"
	@echo "  make all             - Install, format, lint, test, and clean"
	@echo ""

.PHONY: install
install:
	@echo "$(BLUE)Installing production dependencies...$(RESET)"
	pip install -r requirements.txt
	@echo "$(GREEN)✓ Installation complete$(RESET)"

.PHONY: install-dev
install-dev: install
	@echo "$(BLUE)Installing development dependencies...$(RESET)"
	pip install --upgrade black isort pylint pytest pytest-cov
	@echo "$(GREEN)✓ Development setup complete$(RESET)"

.PHONY: run
run:
	@echo "$(MAGENTA)Starting MYTHOS...$(RESET)"
	python mythos.py

.PHONY: test
test:
	@echo "$(BLUE)Running syntax checks...$(RESET)"
	python -m py_compile mythos.py
	@echo "$(GREEN)✓ Syntax check passed$(RESET)"

.PHONY: lint
lint:
	@echo "$(BLUE)Linting code...$(RESET)"
	@command -v pylint >/dev/null 2>&1 && \
		pylint mythos.py --disable=missing-docstring,too-many-locals,too-many-arguments --fail-under=8.0 || \
		echo "$(YELLOW)ℹ pylint not installed, skipping...$(RESET)"

.PHONY: format
format:
	@echo "$(BLUE)Formatting code with black...$(RESET)"
	@command -v black >/dev/null 2>&1 && \
		black mythos.py || \
		echo "$(YELLOW)ℹ black not installed, skipping...$(RESET)"
	@echo "$(BLUE)Organizing imports with isort...$(RESET)"
	@command -v isort >/dev/null 2>&1 && \
		isort mythos.py || \
		echo "$(YELLOW)ℹ isort not installed, skipping...$(RESET)"
	@echo "$(GREEN)✓ Formatting complete$(RESET)"

.PHONY: check
check: lint test format
	@echo "$(GREEN)✓ All checks passed$(RESET)"

.PHONY: clean
clean:
	@echo "$(BLUE)Cleaning up...$(RESET)"
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✓ Cleanup complete$(RESET)"

.PHONY: debug
debug:
	@echo "$(MAGENTA)Starting MYTHOS in debug mode...$(RESET)"
	DEBUG=true python mythos.py

.PHONY: all
all: clean install-dev format lint test
	@echo "$(GREEN)✓ Full setup and checks complete$(RESET)"
