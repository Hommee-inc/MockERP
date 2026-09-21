---
name: mockerp-entity-generation
description: Use for any MockERP provider, helper, model, Entity, Customer, Supplier, address, document, phone, email, or domain-generator work. Always use this skill when generating or changing ERP registrations, provider contracts, or entity relationships so the result follows the entity-generation SOT instead of becoming unrelated mock records.
---

# MockERP Entity Generation

Use this skill to implement coherent entity mock data according to
`docs/sot/entity-generation.md`.

## Read first

Read `AGENTS.md`, `docs/guidelines.md`, `docs/sot/entity-generation.md`, and
the existing provider and generator files being changed.

## Core separation

```text
Faker library       → isolated fake values
Provider            → capability adapter
Generic helper      → one reusable value operation
EntityGenerator     → common registration data
CustomerGenerator   → customer-specific data
SupplierGenerator   → supplier-specific data
Notebook / Job      → execution and orchestration
```

Do not let a specialized generator regenerate the base entity. Reuse the same
entity object when composing a role:

```python
entity = generate_entity()
customer = generate_customer(entity)
supplier = generate_supplier(entity)
```

## Mandatory generator configuration

Every `generate_*` function **must** receive a configuration object or
dictionary. This is a required API contract for all current and future
generators, even when a particular generator does not currently use every
configuration field.

Use this shared shape:

```python
config = {
    "locale": "pt_BR",
    "seed": 42,
    "data_quality_mode": "clean",
}
```

`data_quality_mode` must support these values:

- `clean`: preserve all normal guardrails;
- `dirty`: reserved for explicitly configured duplicate or invalid-data
  scenarios used by payload and ETL tests.

The `dirty` mode does not need to remove guardrails yet. It must still exist in
the configuration contract now, so adding dirty-data behavior later does not
require changing every generator signature. Never add separate ad-hoc flags
such as `dirt`, `skip_validation`, or `allow_bad_data` when the behavior
belongs in this shared configuration.

Generators must propagate the same `config` to dependent generators instead of
creating a new configuration implicitly.

## Base Entity boundary

The base entity owns identification, name, social or trade name, main phones,
main structured address, emails, RG or state registration, and issuing state.
The first implementation is Brazil-specific: CPF for individuals, CNPJ for
legal entities, and Brazilian registration data.

## Provider contracts

Use capability contracts:

- `NameProvider.name()`;
- `EmailProvider.email()`;
- `AddressProvider.address()`;
- `PhoneProvider.phone()`;
- `DocumentProvider.document(document_type)`.

Generators depend on contracts rather than Faker. A document provider must
reject unsupported document types with a clear `ValueError`.

## Generator rules

- Every `generate_*` function receives a shared `config` object or dictionary.
- Use `config["data_quality_mode"]` with `clean` as the default and `dirty` as
  an explicit opt-in for configured bad data.
- Do not use ambiguous flags such as `dirt` when a data-quality mode explains
  the behavior.
- Generate stable IDs outside Faker.
- Treat CPF/CNPJ as a unique business key in clean generation, even though it
  is not the primary key.
- Track issued identifiers during a generation run and reject collisions.
- Allow duplicate identifiers only through an explicit anomaly or ETL-test
  mode; never silently weaken clean-data generation.
- Pass source entities or valid IDs into dependent generators.
- Calculate derived values from source records.
- Do not randomly recreate values that already exist in a source entity.
- Accept a seed when randomness affects output.
- Keep customer and supplier fields out of the base entity.
- Keep generic helpers free of customer or supplier business rules.

## Implementation workflow

1. Identify whether the field belongs to the base entity or a role.
2. Identify the provider capability required for its raw value.
3. Add or reuse the smallest contract needed.
4. Implement the provider adapter.
5. Implement the generator or model without importing Faker directly.
6. Add tests for schema, reuse, relationships, and unsupported inputs.
7. Update the SOT when a durable boundary or schema decision changes.

## Required validation

Validate provider contracts, entity schema, specialization reuse, document
types, seed reproducibility, and local execution without a Databricks runtime.
