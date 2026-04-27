# Makefile — project task runner
# Quality Gate target (`make check`) implements the gate defined in CLAUDE.md §Quality Gate.
# All targets are phony (none produce files).

.DEFAULT_GOAL := help

.PHONY: help check lint format format-check typecheck \
        test-smoke test-contract test-integration test-fuzz test-all clean

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*##"}; {printf "  %-16s %s\n", $$1, $$2}'

# ── Quality Gate ───────────────────────────────────────────────────────────────
# Runs all four checks and reports every failure before exiting.
# pytest exit code 5 ("no tests collected") is treated as a pass — expected
# during early stages when test files don't exist yet. Any other non-zero
# exit code from pytest is a real failure and propagates.
check: ## Run full quality gate: lint, format-check, typecheck, smoke tests
	@echo "── lint ──────────────────────────────────────────────────"; \
	poetry run ruff check .;            LINT=$$?; \
	echo "── format-check ──────────────────────────────────────────"; \
	poetry run ruff format --check .;   FMT=$$?; \
	echo "── typecheck ─────────────────────────────────────────────"; \
	poetry run mypy adapters framework models tests; MYPY=$$?; \
	echo "── test: smoke ───────────────────────────────────────────"; \
	poetry run pytest -m smoke; PYTEST=$$?; \
	[ $$PYTEST -eq 5 ] && PYTEST=0; \
	echo "──────────────────────────────────────────────────────────"; \
	if [ $$LINT -ne 0 ] || [ $$FMT -ne 0 ] || [ $$MYPY -ne 0 ] || [ $$PYTEST -ne 0 ]; then \
		echo "Quality gate FAILED"; exit 1; \
	else \
		echo "Quality gate PASSED"; \
	fi

# ── Individual checks ──────────────────────────────────────────────────────────
lint: ## Run ruff linter
	poetry run ruff check .

format: ## Apply ruff formatter (modifies files)
	poetry run ruff format .

format-check: ## Check formatting without modifying files
	poetry run ruff format --check .

typecheck: ## Run mypy --strict type checker
	poetry run mypy adapters framework models tests

# ── Test suites ────────────────────────────────────────────────────────────────
test-smoke: ## Run smoke suite (@pytest.mark.smoke)
	poetry run pytest -m smoke

test-contract: ## Run contract suite (@pytest.mark.contract)
	poetry run pytest -m contract

test-integration: ## Run integration suite (@pytest.mark.integration)
	poetry run pytest -m integration

test-fuzz: ## Run fuzz suite (@pytest.mark.fuzz)
	poetry run pytest -m fuzz

test-all: ## Run all four suites in sequence
	poetry run pytest -m "smoke or contract or integration or fuzz"

# ── Housekeeping ───────────────────────────────────────────────────────────────
clean: ## Remove all tool caches and __pycache__ directories
	rm -rf .pytest_cache .mypy_cache .ruff_cache .hypothesis
	find . -type d -name __pycache__ -not -path './.venv/*' -exec rm -rf {} +
