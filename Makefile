.PHONY: help install unit ruff format mypy lint check build clean
.DEFAULT_GOAL := help

# Release version for `make build`, like 1.4.0
VERSION ?=

help:
	@echo "make install               Install dependencies into .venv"
	@echo "make unit                  Run unit tests with coverage"
	@echo "make ruff                  Check style with ruff"
	@echo "make format                Fix style with ruff"
	@echo "make mypy                  Check types with mypy"
	@echo "make lint                  Run all linters"
	@echo "make check                 Validate skills against the schema and the latest tag"
	@echo "make build VERSION=1.4.0   Write skills.json"
	@echo "make clean                 Remove generated files"

install:
	uv sync --locked

unit:
	uv run pytest

ruff:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff check --fix .
	uv run ruff format .

mypy:
	uv run mypy

lint: ruff mypy

check:
	rm -rf tmp/previous
	mkdir -p tmp/previous/src
	tag=$$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || true); \
	if [ -n "$$tag" ]; then \
		echo "Comparing with $$tag"; \
		git archive "$$tag" src | tar -x -C tmp/previous; \
	fi
	uv run python -m catalog check --source src --previous tmp/previous/src

build:
	uv run python -m catalog build --source src --version "$(VERSION)" --output skills.json

clean:
	rm -rf tmp .hypothesis .coverage .mypy_cache .pytest_cache .ruff_cache skills.json
