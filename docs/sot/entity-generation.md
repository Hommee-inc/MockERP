# MockERP entity-generation decisions

Status: authoritative

This is the reference for registrations, customers, suppliers, and the
provider boundary. When implementation and this document disagree, update the
decision first or document why it changed.

## Purpose

MockERP starts with Brazilian registration data and should be able to grow to
other countries later. The goal is a coherent base entity that can be reused by
different business roles without duplicating its common data.

## Domain model

```text
Entity
├── shared registration data
├── Customer role
├── Supplier role
└── future business roles
```

An entity can represent either an individual (CPF) or a legal entity (CNPJ).
The base entity must not contain customer-only or supplier-only fields.

## Generation contract

Every generator receives the same configuration object:

```python
config = {
    "locale": "pt_BR",
    "seed": 42,
    "data_quality_mode": "clean",
}
```

`clean` is the default and preserves normal guardrails. `dirty` is opt-in for
explicit anomaly scenarios. It does not automatically disable every check.
Each relaxed rule must be named, documented, and tested.

The intended flow is:

```text
generate_entity(config, entity_id)
          ↓
shared registration data
          ├── generate_customer(config, entity)
          └── generate_supplier(config, entity)
```

`generate_entity()` creates only common registration data. A specialization
adds its own fields to the existing entity; it must not regenerate the name,
document, contacts, or address.

The same entity may support more than one role if the business model allows it:

```python
entity = generate_entity(config, entity_id=1)
customer = generate_customer(config, entity)
supplier = generate_supplier(config, entity)
```

## Base entity schema

The first version uses this schema:

```text
entity_id
entity_type
identification
name
social_name
main_phone
main_mobile
main_address
emails
state_registration_rg
state_registration_issuer
```

For the current Brazilian implementation:

| Entity type | Identification | Name | Social name | Registration field |
|---|---|---|---|---|
| Individual | CPF | Full name | Social name | RG |
| Legal entity | CNPJ | Legal name | Trade name | State registration |

The field names remain generic so the model can later support other document
systems.

## Identifications

The internal entity ID is the primary key. CPF/CNPJ is a business identifier:

```text
Entity PK              → stable internal ID
Entity identification  → CPF or CNPJ
```

In `clean` mode, identifiers must be unique within the generation run. The
generator keeps a run-local registry for that purpose. Duplicate identifiers
are valid only when a named anomaly or duplicate-injection scenario requests
them.

Document selection belongs behind the document provider capability. Customer
and supplier generators should not know how CPF or CNPJ is formatted.

## Contacts and address

The base entity owns shared contact data:

- `main_phone` is the primary general phone;
- `main_mobile` is the primary mobile phone;
- `emails` can contain multiple addresses, separated by `;` for now;
- `main_address` is a structured object.

The initial address shape is:

```text
street
postal_code
city
state
district
country
```

Email and address normalization may happen later, but ownership must stay with
the base entity.

## Provider boundary

A provider answers how a value is obtained. A generator answers what the
record means.

The current contracts are:

```text
NameProvider
EmailProvider
AddressProvider
PhoneProvider
DocumentProvider
```

`FakerProvider` implements them today. A future provider could use reference
data or another library without changing entity or role generation.

Providers produce values; they do not decide whether a budget converts, a sale
is confirmed, or a return is valid.

## Package direction

```text
Domain generators
        ↓
Provider contracts
        ↓
Provider implementations
        ↓
Faker or another value source
```

Domain generators depend on contracts. Provider implementations satisfy those
contracts. The generator layer must not import `faker.Faker` directly.

## Intended package layout

```text
src/mockerp/
├── providers/
│   ├── provider_contract.py
│   └── faker_provider.py
├── generators/
│   ├── entity.py
│   ├── customer.py
│   ├── supplier.py
│   └── generic capabilities
└── models/
    ├── entity.py
    └── address.py
```

Some entries are future structure, not a claim that every file exists today.

## Invariants

- specializations reuse an existing entity;
- clean CPF/CNPJ values are unique;
- duplicate identifiers require an explicit anomaly mode;
- every generator receives and propagates `config`;
- generic capabilities do not contain business rules;
- providers do not contain customer or supplier rules;
- the base entity owns shared registration data;
- the generator remains testable without Databricks.

## Deferred decisions

The first version does not define final customer or supplier commercial terms,
normalized contact tables, international document rules, or external reference
data. Those can be added later without changing the boundaries above.
