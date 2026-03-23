# TREEMOR Makefile

.PHONY: install test clean build docs deploy

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=treomor --cov-report=html

lint:
	black treomor tests
	isort treomor tests
	flake8 treomor tests

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:
	python -m build

docs:
	cd docs && make html

deploy:
	git push origin main
	git push gitlab main

help:
	@echo "Available commands:"
	@echo "  make install     - Install package"
	@echo "  make install-dev - Install with dev dependencies"
	@echo "  make test        - Run tests"
	@echo "  make lint        - Run linters"
	@echo "  make clean       - Clean build files"
	@echo "  make build       - Build distribution"
	@echo "  make docs        - Build documentation"
