# Microservice API Testing Framework

Production-quality API testing framework for microservices, built around OOP client design, OpenAPI contract testing, and suite-based automation.

---

## What This Is

A reusable, environment-aware API testing framework. [Petstore v3 (OpenAPI 3.0)](https://petstore3.swagger.io/api/v3/openapi.json) is the learning vehicle — it exercises the full framework across Pet, Store, and User resources without requiring real auth or private services. The architecture is designed to scale to 13+ real microservices once the patterns are proven. Everything substantive — conventions, architecture, workflow rules — lives in [CLAUDE.md](./CLAUDE.md).

## Tech Stack

- Python 3.12+, Poetry
- `httpx` (HTTP client), `pydantic v2` (models and validation)
- `pytest`, `schemathesis` (contract + fuzz testing), `allure-pytest` (reporting)
- `python-dotenv` (env-based config), Python `logging` (structured logs with redaction)
- `ruff` (lint + format), `mypy --strict` (type checking)

## Quick Start

```bash
git clone https://github.com/SaiVamsiKolla-QA/microservice-api-testing.git
cd microservice-api-testing
poetry install
cp .env.example .env.qa
# edit .env.qa with real values if needed
ENV=qa make test-smoke
```

`ENV=qa` tells the framework which `.env.<ENV>` file to load. It defaults to `qa` if unset. See `.env.example` for all required variables.

## Make Targets

| Target | Description |
|---|---|
| `make help` | List all available targets |
| `make check` | Run the full Quality Gate (lint, format, typecheck, smoke) |
| `make test-smoke` | Run smoke suite |
| `make test-contract` | Run contract suite |
| `make test-integration` | Run integration suite |
| `make test-fuzz` | Run fuzz suite |
| `make test-all` | Run all four suites |

## Project Structure

```
microservice-api-testing/
├── adapters/        # HTTP clients (one per resource)
├── framework/       # Config, logger, assertions, reporting
├── models/          # Pydantic models mirroring API schemas
├── tests/           # Test suites (smoke, contract, integration, fuzz)
├── specs/           # Local OpenAPI specs (petstore.yaml)
├── scripts/         # run_suite.sh, diff_specs.py, signoff.py
├── testdata/        # Test fixtures and expected JSON schemas
├── runs/            # Per-env test output (gitignored)
├── docs/            # Architecture and test strategy docs
├── .env.example     # Config template
├── Makefile         # Task runner
└── pyproject.toml   # Dependencies and tool config
```

## Where to Go Next

- [CLAUDE.md](./CLAUDE.md) — full project rules, architecture, layer responsibilities, workflow, coding standards
- [docs/architecture.md](./docs/architecture.md) — architecture deep-dive _(forthcoming)_
- [docs/test-strategy.md](./docs/test-strategy.md) — test strategy _(forthcoming)_

## License

MIT — see [LICENSE](./LICENSE)
