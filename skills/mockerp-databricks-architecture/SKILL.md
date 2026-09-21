---
name: mockerp-databricks-architecture
description: Use for any MockERP architecture, package layout, Databricks notebook or Job, dependency, Free Edition capability, Delta/Parquet boundary, or layer-placement decision. Always use this skill when deciding where MockERP code belongs or when a request mentions Databricks execution, even if the user does not explicitly ask for an architecture review.
---

# MockERP Databricks Architecture

Use this skill to keep MockERP production-style without assuming paid
Databricks capabilities.

## Read first

Read `AGENTS.md`, `docs/architecture.md`, `docs/guidelines.md`, the entity
SOT when entities are involved, and the relevant roadmap document.

## Layer placement

| Concern | Location |
|---|---|
| Package metadata | `pyproject.toml` |
| Provider contracts | `src/mockerp/providers/provider_contract.py` |
| Fake-library adapters | `src/mockerp/providers/` |
| Generators | `src/mockerp/generators/` |
| Data models | `src/mockerp/models/` |
| Databricks orchestration | `notebooks/` or Jobs |
| Tests | `tests/` |
| Durable decisions | `docs/` and `docs/sot/` |

Do not place reusable business logic only in a notebook. Do not import
`faker.Faker` directly from a domain generator.

## Dependency direction

```text
notebook / Job
    ↓
domain generator
    ↓
provider contract
    ↑
provider implementation
```

The notebook may configure and call the package. It must not recreate entity
rules, relationship logic, or provider implementations.

## Free Edition boundary

Treat Databricks Free Edition as a constrained execution target. Before using
Jobs, compute features, Unity Catalog, Volumes, package installation,
networking, external APIs, quotas, or persistence features:

1. verify that the capability exists in the current workspace;
2. document the assumption and limitation;
3. provide a local or manual fallback when practical;
4. keep domain generators independent of the platform.

Never claim that a Databricks operation was validated when it was only reasoned
about locally.

## Dependency policy

- Declare Python dependencies in `pyproject.toml`.
- `%pip install` may be used for temporary Free Edition development.
- Do not make repeated notebook installation the permanent package strategy.
- Keep the package runnable and testable outside the Databricks runtime.

## Required output for architecture changes

Report the selected layer, dependency direction, Databricks capability,
Free Edition validation status, documentation updated, and tests executed.
