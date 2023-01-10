.DEFAULT_GOAL := help

.PHONY: help
help: ## Show help information
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

.PHONY: deps
deps: ## Install dependencies and Git hooks
	poetry install
	poetry run pre-commit install

.PHONY: lint
lint: ## Code analyse and lint
	poetry run pylint tests/ hooks/

.PHONY: test
test: ## Test in current Python version
	poetry run pytest

.PHONY: clean
clean: ## Clean up cache files
	rm -rf .pytest_cache/
