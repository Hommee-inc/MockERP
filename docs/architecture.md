# MockERP — Project Architecture

The rules for keeping entities coherent are defined in
[guidelines.md](guidelines.md). This document defines where code belongs; the
guidelines define how data must relate.

The authoritative entity-generation model is defined in
[`sot/entity-generation.md`](sot/entity-generation.md).

The one-time Databricks dependency setup is defined in
[`databricks-environment.md`](databricks-environment.md).

## Execution context

The current target is **Databricks Free Edition**. The project follows
production-style patterns—Python packaging, declared dependencies, testable
generators, and thin notebooks—but execution may be limited by the features
available in this edition.

```text
Reusable domain code       →  src/mockerp/
Available execution       →  Databricks Free Edition
Advanced capabilities     →  only after workspace validation
```

Jobs, compute, Unity Catalog, Volumes, package installation, networking,
quotas, and persistence must be treated as capabilities to validate, not as
platform guarantees. The same generator should remain runnable locally for
development and testing when necessary.

## Responsibility tree

```text
MockERP/
├── pyproject.toml                 # Package, dependencies, and build
├── README.md                      # Project entry point
├── LICENSE
├── AGENTS.md                      # Agent and contribution rules
├── skills/                        # MockERP-only operational skills
│   ├── mockerp-databricks-architecture/
│   ├── mockerp-entity-generation/
│   └── mockerp-databricks-validation/
├── docs/
│   ├── architecture.md            # This document
│   ├── guidelines.md              # Data-coherence rules
│   └── Roadmap/                   # Functional and technical evolution
├── src/mockerp/                   # Reusable Python package
│   ├── __init__.py
│   ├── providers/                 # Adapters for fake-data libraries
│   │   ├── __init__.py
│   │   ├── provider_contract.py   # Provider contracts
│   │   └── faker_provider.py      # Faker-backed implementation
│   └── generators/                # ERP mock-data construction
│       ├── __init__.py
│       ├── config.py               # Shared generator configuration
│       ├── entity.py               # Base registration generation
│       └── customer.py             # Customer generation
├── notebooks/                     # Databricks orchestration and usage
│   ├── customer/
│   ├── person/
│   ├── records/
│   └── helpers/                   # Prototyping and exploration
└── tests/                         # Python package tests
```

## Call flow

```text
Databricks notebook / Job
          │
          ▼
src/mockerp/generators/customer.py
          │ uses contracts
          ▼
src/mockerp/providers/provider_contract.py
          │ implemented by
          ▼
src/mockerp/providers/faker_provider.py
          │ adapts
          ▼
Faker library (pt_BR)
```

## Fake library versus mock data

```text
Faker library
  └── produces isolated values: names, emails, documents, addresses

FakerProvider
  └── exposes those values through MockERP contracts

CustomerGenerator
  └── combines values, IDs, statuses, and ERP domain rules
      └── produces a valid customer record for the dataset
```

- **Fake data** consists of artificial values used as raw material, usually
  produced by a library such as Faker.
- **Mock data** consists of structured artificial records that simulate a real
  system through schemas, relationships, IDs, states, and business rules.
- **MockERP** is not just a collection of Faker values; it is a simulated ERP
  with entities and relationships.

## Layer responsibilities

### Providers

Providers adapt fake-data libraries and produce individual values. They do not
assemble complete ERP entities or know ERP business rules.

`provider_contract.py` defines the contracts:

- `NameProvider.name()`
- `EmailProvider.email()`
- `AddressProvider.address()`
- `PhoneProvider.phone()`
- `DocumentProvider.document(document_type)`

`faker_provider.py` implements these contracts by delegating to
`Faker("pt_BR")`.

### Generators

Generators assemble ERP mock data using providers. They own entity schemas,
relationships, and domain rules, but must not import `faker.Faker` directly.

Example:

```python
from mockerp.generators import generate_customer

config = {"locale": "pt_BR", "seed": 42, "data_quality_mode": "clean"}
customer = generate_customer(config, customer_id=1)
```

### Notebooks

Notebooks and Jobs are Databricks entry points. They configure parameters, call
the package, display results, and write Delta or Parquet data. They must not
duplicate providers, generators, or relationship rules.

### Tests

Tests validate provider contracts, record schemas, relationships, and business
invariants. External dependencies are declared in `pyproject.toml`, not
repeated `%pip install` commands in every production notebook.

## Dependency direction

```text
notebooks/jobs ──> generators ──> provider contracts <── provider implementations
                         └──────> domain rules
```

Dependencies should point downward. A provider must not import a generator,
and a generator must not import `faker.Faker` directly.
