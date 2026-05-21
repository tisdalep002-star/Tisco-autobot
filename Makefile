.PHONY: help install run clean lint format

help:
	@echo "MYTHOS Development Tasks"
	@echo ""
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make run        - Run MYTHOS"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Lint code"
	@echo "  make format     - Format code"
	@echo "  make clean      - Clean up cache files"
	@echo "  make help       - Show this help message"

install:
	pip install -r requirements.txt

run:
	python mythos.py

test:
	python -m py_compile mythos.py
	@echo "✓ Syntax check passed"

lint:
	@command -v pylint >/dev/null 2>&1 && pylint mythos.py --disable=missing-docstring,too-many-locals,too-many-arguments || echo "pylint not installed, skipping..."

format:
	@command -v black >/dev/null 2>&1 && black mythos.py || echo "black not installed, skipping..."
	@command -v isort >/dev/null 2>&1 && isort mythos.py || echo "isort not installed, skipping..."

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Cleaned up cache files"
