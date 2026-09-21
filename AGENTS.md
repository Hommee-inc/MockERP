# MockERP — Agent Guidelines

## Language rule

All repository artifacts must be written in English: source code, comments,
docstrings, documentation, tests, notebooks, schemas, labels, and commit
messages. User requests may use any language, but implementation output must be
English.

## Before changing the project

Read these documents in order:

1. [`README.md`](README.md) — project purpose;
2. [`docs/architecture.md`](docs/architecture.md) — structure and dependencies;
3. [`docs/guidelines.md`](docs/guidelines.md) — data-coherence rules;
4. [`docs/sot/entity-generation.md`](docs/sot/entity-generation.md) —
   authoritative entity-generation decisions;
5. the roadmap document for the version being implemented.

When a task matches a project-local skill under `skills/`, read and follow
that skill as well.

Do not implement an entity in isolation. Understand its dependencies and which
future entities will depend on it.

## Target platform: Databricks Free Edition

The project targets Databricks Free Edition. It teaches production-style
patterns, but paid or enterprise features must not be assumed to exist.
Validate compute, Jobs, Unity Catalog, Volumes, Delta persistence, package
installation, networking, quotas, and runtime limits in the current workspace.

If a capability is unavailable, keep domain code separate from the platform
layer and document a local or manual alternative. Never claim that an
unvalidated Databricks step was executed.

## Required architecture

```text
Databricks notebook / Job
          ↓
src/mockerp/generators/
          ↓
src/mockerp/providers/provider_contract.py
          ↑
src/mockerp/providers/*_provider.py
```

- Providers produce individual fake values.
- Generators assemble mock data with schemas, IDs, and business rules.
- Notebooks orchestrate execution, parameters, and persistence.
- Tests prove contracts and invariants.

Generators must not import `faker.Faker` directly. Use provider contracts and
dependency injection.

## Data rules

- Every entity must have a stable primary key.
- Foreign keys must point to existing records.
- Dependent entities must be created from their source entities.
- Totals, quantities, and derived values must be calculated, not re-randomized.
- The same seed must reproduce the same scenario.
- The v0.1–v0.4 golden dataset must be consistent.
- Anomalies are applied in a separate layer starting with v0.5.

## New-entity workflow

1. Read the corresponding roadmap.
2. Define the primary key and foreign keys.
3. Identify the source entity and generation order.
4. Create or reuse provider contracts.
5. Implement the generator in `src/mockerp/generators/`.
6. Add schema, relationship, and business-rule tests.
7. Update architecture and guidelines when the design changes.
8. Update the roadmap checklist when the delivery is complete.

## Dependencies and validation

- Keep Python dependencies in `pyproject.toml`.
- `%pip install` is acceptable for temporary Free Edition development, but not
  as the permanent dependency strategy for production notebooks.
- Keep shared code in `src/mockerp/`, never only in notebook cells.
- Run `python -m compileall -q src tests` and `pytest tests/ -v` when possible.
- If a dependency is unavailable, document the limitation; do not remove tests.

## Git rules

- Do not commit `__pycache__/`, `*.pyc`, `.pytest_cache/`, or virtual environments.
- Never commit credentials, tokens, personal data, or real datasets.
- Commit messages must describe the functional or structural change.
- Preserve unrelated existing changes.
