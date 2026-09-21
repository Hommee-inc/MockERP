# MockERP data guidelines

These rules keep MockERP coherent as an ERP dataset instead of turning it into
several unrelated collections of fake records.

## What “coherent” means here

Every record needs an identity, a place in the domain, and a reason for its
values to exist. If a sale is created independently from its budget, or if an
inventory movement gets a new random quantity, the dataset may look plausible
but it no longer represents a system.

The basic rule is:

```text
Faker produces values
Providers adapt those values
Generators create entities
Relationships come from source records
Tests prove the important invariants
```

## Shared configuration

All generators receive the same configuration object:

```python
config = {
    "locale": "pt_BR",
    "seed": 42,
    "data_quality_mode": "clean",
}
```

`clean` is the default. It keeps normal validations enabled. `dirty` is an
explicit mode for named anomaly scenarios; it must not mean “turn off every
check”. Each relaxed rule needs a reason and a test.

## Identity and business identifiers

Each entity gets its own stable primary key:

- `entity_id` for the common registration;
- `customer_id` for customers;
- `product_id` for products;
- `budget_id` for budgets;
- `sale_id` for sales;
- `return_id` for returns.

Names and Faker values are not primary keys. CPF and CNPJ are business
identifiers. In a clean run they must be unique, but they are still separate
from the internal primary key. Duplicates belong in an explicit anomaly mode,
never in the default dataset by accident.

## Relationships are created at the source

Dependent records should receive the source record they need:

```text
Customer
   ↓
Budget.customer_id
   ↓
Sale.budget_id + Sale.customer_id
   ↓
Return.sale_id
```

Do not generate a sale and a customer independently and then choose a random
customer ID. That hides the dependency and makes invalid foreign keys likely.

The full generation order is:

```text
customers/products
        ↓
budgets + items
        ↓
sales + items
        ↓
returns + items
        ↓
inventory and finance
```

## Derived values come from source documents

If a value already exists upstream, downstream records copy or calculate it:

- a sale gets its customer from the budget;
- a sale total is the sum of its items;
- inventory exits come from sold quantities;
- receivables come from sale values;
- refunds come from return values.

Generating a second random value for any of these creates inconsistencies that
are difficult to explain and impossible to reconcile reliably.

## Providers and generators have different jobs

Providers may know how to produce a name, CPF, address, or phone. They must not
know whether a budget was converted or whether a return is valid.

Generators own the business decisions: allowed statuses, creation order,
relationships, totals, dates, and quantity limits. This separation also makes
it possible to replace Faker later without rewriting the domain rules.

## Reproducibility

The same configuration and seed should produce the same scenario. Reproducible
data makes debugging, tests, notebook comparisons, and quality exercises much
easier.

## Anomalies are a separate layer

The golden dataset through v0.5 should be internally consistent. Starting in
v0.6, anomalies are applied after the clean dataset is generated:

```text
clean golden dataset
          ↓
configured anomaly
          ↓
dataset with a known issue
```

Examples include duplicate records, missing relationships, invalid references,
negative stock, and mismatched documents. Each injected issue should be
recorded so a later quality pipeline can be checked against a known answer.

## What tests should prove

Tests should check the rules that make the data useful:

- every foreign key points to an existing record;
- every generated ID is valid and stable within the dataset;
- clean CPF/CNPJ values are unique;
- totals equal the sum of their items;
- event dates follow the expected order;
- statuses belong to the allowed set;
- returned quantities do not exceed sold quantities;
- the same seed reproduces the same scenario.

## Adding a new entity

Before implementing one, answer these questions:

1. What is its primary key?
2. Which existing entity creates it?
3. Which foreign keys does it carry?
4. Which values are copied or calculated?
5. What is the generation order?
6. Which invariants need tests?
7. Which future roadmap step depends on it?

The generator, tests, and relationship documentation should be added together.
