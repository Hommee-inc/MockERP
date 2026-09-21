# MockERP

MockERP is a small synthetic ERP laboratory built to practice data engineering
with data that behaves more like a real business system than a random table of
fake values.

The project generates Brazilian registration and commercial data with stable
identifiers, relationships, business rules, and reproducible scenarios. The
long-term goal is to use the dataset in Python, SQL, Databricks, pipelines,
quality checks, and BI exercises without relying on production data.

> This project is actively evolving. The current implementation covers the
> foundation and the first customer/entity generators; the broader ERP modules
> are documented in the roadmap.

## Why this project exists

Many mock datasets are useful for testing a column or a chart, but they do not
behave like a system of record. MockERP focuses on the connections between
records:

- a business entity has its own internal ID;
- CPF/CNPJ is treated as a business identifier, not as the primary key;
- customer and company data share a reusable base entity;
- dependent records are created from their source records;
- clean data keeps its normal guardrails;
- future anomalies will be injected in a separate, documented layer.

This makes it possible to test not only ingestion, but also referential
integrity, reconciliation, deduplication, and data-quality workflows.

## Current scope

The current version includes:

- a provider layer backed by `Faker("pt_BR")`;
- provider contracts for names, emails, addresses, phones, and documents;
- generation of individual and legal-entity registrations;
- customer generation through dependency injection;
- unique CPF/CNPJ values in a clean generation run;
- deterministic output when the same seed is used;
- tests for schemas, configuration validation, uniqueness, and reproducibility;
- a Databricks-oriented project structure while keeping the domain package
  runnable locally.

The planned commercial flow is:

```text
Customer / Product
        ↓
Budget → Sale → Return
        ↓       ↓
    Inventory  Finance
```

## Architecture

```text
Databricks notebook or job
            ↓
src/mockerp/generators/
            ↓
src/mockerp/providers/provider_contract.py
            ↑
src/mockerp/providers/faker_provider.py
```

The boundaries are intentional:

- **Providers** produce individual values and hide the fake-data library.
- **Generators** assemble entities and enforce domain rules.
- **Notebooks** configure and orchestrate execution.
- **Tests** verify schemas, relationships, and invariants.

Generators do not import `faker.Faker` directly. This keeps the domain code
independent from the current provider and makes alternative providers possible
later.

## Project layout

```text
MockERP/
├── src/mockerp/
│   ├── generators/       # Entity and customer generation
│   └── providers/        # Contracts and Faker adapter
├── tests/                # Generator and provider tests
├── notebooks/            # Databricks entry points and experiments
├── docs/
│   ├── architecture.md
│   ├── guidelines.md
│   ├── sot/              # Authoritative domain decisions
│   └── Roadmap/          # Version-by-version implementation plan
└── pyproject.toml
```

## Quick start

The package requires Python 3.10 or newer.

```powershell
python -m venv .venv
\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

Generate a reproducible entity:

```python
from mockerp.generators import generate_entity

config = {
    "locale": "pt_BR",
    "seed": 42,
    "data_quality_mode": "clean",
}

entity = generate_entity(config, entity_id=1, entity_type="individual")
print(entity)
```

Run the test suite:

```powershell
python -m compileall -q src tests
pytest tests/ -v
```

## Data-quality modes

Every generator receives the same configuration shape:

```python
{
    "locale": "pt_BR",
    "seed": 42,
    "data_quality_mode": "clean",
}
```

`clean` is the default and preserves the normal validation rules. `dirty` is
reserved for explicit, named anomaly scenarios. It must never silently disable
all validation at once.

## Roadmap

The roadmap is intentionally incremental:

1. **v0.1 — Foundation:** registrations, providers, and customer generation.
2. **v0.2 — Commercial core:** budgets, sales, and returns.
3. **v0.3 — Inventory:** stock entries, exits, and traceable movements.
4. **v0.4 — Finance:** accounts receivable, payments, and refunds.
5. **v0.5 — Integration:** cross-module consistency checks.
6. **v0.6 — Controlled errors:** duplicates, invalid relationships, and
   document mismatches applied on top of a clean dataset.
7. **v1.x — Databricks platform:** Bronze, Silver, Gold, incremental ingestion,
   schema evolution, merges, history, and orchestration.
8. **v2.0 — Public lab:** reusable scenarios, documentation, and a final
   dashboard.

See [`docs/Roadmap/00-mockerp-overview.md`](docs/Roadmap/00-mockerp-overview.md) for
the full plan.

## Databricks note

The target platform is Databricks Free Edition. The repository keeps the
domain logic independent from the platform so it can be developed and tested
locally. Jobs, persistence, Unity Catalog, Volumes, networking, and other
workspace capabilities are treated as items to validate in the target
environment rather than assumed features.

## Portfolio summary

> Built a reproducible synthetic ERP data generator in Python with a layered
> provider/generator architecture, dependency injection, stable identifiers,
> referential-integrity rules, automated tests, and a roadmap for Databricks
> Bronze/Silver/Gold data-quality workflows.

## License

This project is available under the terms of the [MIT License](LICENSE).
