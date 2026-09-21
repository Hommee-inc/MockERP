---
name: mockerp-databricks-validation
description: Use for MockERP testing, data-quality checks, generator validation, reproducibility checks, notebook/job readiness, Delta/Parquet boundary checks, or Free Edition execution limitations. Always use this skill before declaring a MockERP Databricks feature complete.
---

# MockERP Databricks Validation

Use this skill to validate the Python package and the Databricks execution
boundary without overstating what Free Edition supports.

## Validation order

```text
syntax and imports
  ↓
provider contracts
  ↓
generator schemas
  ↓
domain invariants
  ↓
seed reproducibility
  ↓
notebook/package boundary
  ↓
Databricks capability, if available
```

A local package test is not evidence that a Databricks Job, Volume, catalog,
network call, or Delta write succeeded.

## Local checks

Run when possible:

```powershell
python -m compileall -q src tests
pytest tests/ -v
```

If dependencies are missing, report the exact limitation and keep the test in
place. Do not weaken or remove tests.

## Required domain invariants

Test that:

- every `generate_*` function accepts and propagates `config`;
- clean mode preserves guardrails;
- dirty mode is explicit and relaxes only configured rules;
- primary keys are present and unique;
- CPF/CNPJ identifiers are unique in the clean dataset;
- duplicate CPF/CNPJ values occur only when an anomaly or ETL-test mode is
  explicitly enabled;
- foreign keys point to existing records;
- dependent records originate from valid source records;
- totals equal item sums;
- dates follow event order;
- statuses are allowed;
- quantities and amounts respect source limits;
- customer and supplier roles reuse their base entity;
- unsupported document types fail clearly.

## Reproducibility

For a fixed scenario and seed, generate the dataset twice and compare
normalized records. Inject a clock when time-dependent fields need stable
results.

## Notebook and Job checks

Check that notebooks import the package, expose parameters, avoid duplicated
business rules, identify output locations, and do not assume unavailable Free
Edition capabilities.

## Platform capability report

Record the workspace capability status, runtime and Python version, dependency
installation path, storage/catalog target, Free Edition limitation, and local
fallback. Never convert `unknown` into `available` without validation.

## Completion report

```text
Result: PASS / PARTIAL / BLOCKED

Local checks:
- ...

Domain invariants:
- ...

Databricks checks:
- ...

Known limitations:
- ...

Next action:
- ...
```
