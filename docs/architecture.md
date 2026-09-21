# MockERP architecture

This document explains where the project code belongs and how the pieces fit
together. The data rules themselves live in [`guidelines.md`](guidelines.md),
and the current entity model is described in
[`sot/entity-generation.md`](sot/entity-generation.md).

## The short version

```text
Notebook or job
      ↓
Domain generators
      ↓
Provider contracts
      ↑
Provider implementations
```

The package is designed to run locally during development and to be called by
Databricks notebooks when the platform layer is ready. Databricks Free Edition
is the target environment, but Jobs, Volumes, Unity Catalog, persistence, and
other workspace capabilities still need to be checked in the actual workspace.

## Repository map

```text
MockERP/
├── src/mockerp/
│   ├── generators/       # ERP entities and business rules
│   └── providers/        # Contracts and fake-value adapters
├── tests/                # Contract, schema, and invariant tests
├── notebooks/            # Databricks entry points and experiments
├── docs/                 # Architecture, rules, and roadmap
└── pyproject.toml        # Package metadata and dependencies
```

## Responsibilities

### Providers

Providers answer: “How do I get this value?”

The current adapter uses `Faker("pt_BR")` and exposes small capabilities such
as names, emails, addresses, phones, and Brazilian documents. A provider should
not decide whether a sale is valid or whether a return is allowed.

The contracts are defined in `src/mockerp/providers/provider_contract.py`.
`faker_provider.py` is one implementation of those contracts.

### Generators

Generators answer: “What record should exist, and what rules must it satisfy?”

They assemble values from providers into ERP-shaped records. They own IDs,
relationships, statuses, derived values, and validation rules. A generator must
not import `faker.Faker` directly.

For example, a future sale generator should receive a converted budget and
derive its customer, items, and total from that source. It should not generate
those values again and hope they match.

### Notebooks and jobs

Notebooks are entry points, not a second home for domain logic. They should:

1. receive parameters;
2. create the configuration and provider dependencies;
3. call the generators;
4. display or persist the result.

The reusable code stays in `src/mockerp/`, so it can be tested without a
Databricks runtime.

### Tests

Tests cover more than whether a function returns a dictionary. They should
prove that IDs, foreign keys, totals, dates, statuses, and quantities remain
consistent. The same seed should also produce the same scenario.

## Current call flow

```text
Databricks notebook or local script
              ↓
src/mockerp/generators/customer.py
              ↓
src/mockerp/providers/provider_contract.py
              ↑
src/mockerp/providers/faker_provider.py
              ↓
Faker (pt_BR)
```

The direction matters: generators depend on contracts, while provider
implementations satisfy those contracts. Providers never import generators.

## Planned domain flow

The wider ERP model will be built in dependency order:

```text
Customers and products
          ↓
Budgets and budget items
          ↓
Sales and sale items
          ↓
Returns and return items
          ↓
Inventory and finance
```

This order is not just a diagram. It is how the generators should be written:
a dependent record should be created from the record it depends on.

## Platform boundary

The domain package must remain independent from Databricks-specific behavior.
Databricks is responsible for orchestration and storage; the generators are
responsible for producing coherent records. This separation keeps local tests
useful and prevents an unvalidated workspace feature from becoming a hidden
domain dependency.
