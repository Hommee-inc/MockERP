# MockERP
A synthetic environment that simulates the core of an ERP system (quotes, sales, returns, inventory and receivables), generating fake data end to end along with intentional, documented data-quality issues (duplicates, inconsistencies, invalid relationships, mismatched documents). It's meant to be a reusable practice lab for people studying data engineering, data analysis and BI, without needing access to real production data.

## Architecture

See [docs/architecture.md](docs/architecture.md) for the project tree, layer responsibilities, and dependency flow.

See [docs/guidelines.md](docs/guidelines.md) for the rules that keep the generated data coherent as an ERP rather than a collection of unrelated mock records.

See [docs/sot/entity-generation.md](docs/sot/entity-generation.md) for the
authoritative entity, customer, supplier, provider, and helper-generation
model.

Project-local operational skills are documented in [skills/README.md](skills/README.md).

## Platform context

MockERP targets Databricks Free Edition. The project uses production-style
Python structure, but Databricks capabilities such as compute, Jobs, Unity
Catalog, Volumes, package installation, networking, quotas, and persistence
must be validated in the current workspace before being adopted.
