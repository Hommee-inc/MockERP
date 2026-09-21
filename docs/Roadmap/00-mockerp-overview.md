# MockERP roadmap

MockERP started as a practical way to deepen my Databricks and data-engineering
skills. The idea is simple: build an ERP-shaped dataset that people can use to
practice pipelines, SQL, quality checks, dashboards, and reconciliation without
using production data.

## The central idea

The project should generate a clean scenario first. Known problems are added
later, in a separate layer, so a data-quality pipeline can be tested against a
known answer instead of against random broken data.

Planned anomaly examples include duplicates, missing records, invalid
relationships, schema changes, and mismatched business documents.

## Delivery order

```text
Budget → Sale → Return → Inventory → Finance
```

The versions below build on that sequence:

| Version | Focus |
|---|---|
| v0.1 | Registration foundation and customer generation |
| v0.2 | Commercial core: budgets, sales, and returns |
| v0.3 | Inventory movements and stock balance |
| v0.4 | Receivables, payments, and refunds |
| v0.5 | Cross-module integration and reconciliation |
| v0.6 | Controlled data-quality issues |
| v1.0 | Databricks Bronze ingestion |
| v1.1 | Silver cleaning, validation, and quarantine |
| v1.2 | Gold metrics and reconciliation |
| v1.3 | Incremental ingestion, schema evolution, merges, history, and jobs |
| v2.0 | Public lab, documentation, and dashboard |

Each version has its own notes in this folder. They are plans and learning
targets, not claims that every item has already been implemented.
