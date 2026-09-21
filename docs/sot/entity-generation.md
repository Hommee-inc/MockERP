# MockERP SOT — Entity and Registration Generation

Status: authoritative

This document is the source of truth for the generic entity, customer, and
supplier generation model. It defines the boundaries that generators and
providers must preserve.

## 1. Purpose

MockERP must generate coherent ERP registration data, not unrelated random
records. The first implementation targets Brazil and must be extensible to
other countries later.

## 2. Domain model

`Entity` is the base registration shared by people and organizations.

```text
Entity
├── common registration data
├── Customer specialization
├── Supplier specialization
└── future business specializations
```

An entity may represent:

- an individual identified by CPF;
- a legal entity identified by CNPJ.

The base entity must not contain customer-specific or supplier-specific
business fields.

## 3. Separation of responsibilities

Every `generate_*` function must receive a configuration object or dictionary.
The same configuration is propagated through the generation pipeline instead
of scattering locale, seed, and quality parameters across function signatures.

The initial configuration contract is:

```python
config = {
    "locale": "pt_BR",
    "seed": 42,
    "data_quality_mode": "clean",
}
```

`data_quality_mode` must be either:

- `clean` — preserve normal guardrails and business invariants;
- `dirty` — explicitly enable configured invalid or duplicate data for payload
  and ETL tests.

`clean` is the default when the configuration omits the field. `dirty` must not
mean that every validation is disabled automatically. Each relaxed guardrail
must be explicit, named, and testable.

```text
generate_entity()
        ↓
common registration data
        ├───────────────┐
        ↓               ↓
generate_customer()  generate_supplier()
        ↓               ↓
customer data       supplier data
```

### `generate_entity()`

Generates only the common registration record.

### `generate_customer(config, entity)`

Adds only customer-specific data to an existing entity. It must not regenerate
the entity's name, document, contact information, or address.

### `generate_supplier(config, entity)`

Adds only supplier-specific data to an existing entity. It must not regenerate
the entity's common registration data.

The same base entity may be passed to more than one specialization:

```python
config = {"locale": "pt_BR", "seed": 42, "data_quality_mode": "clean"}
entity = generate_entity(config, entity_id=1)
customer = generate_customer(config, entity)
supplier = generate_supplier(config, entity)
```

Whether a real ERP scenario permits both roles is a domain decision; the
architecture must support reuse without duplicating the base registration.

## 4. Base entity schema

The initial `Entity` record must contain at least:

```text
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

The initial implementation is Brazil-specific:

| Entity type | `identification` | `name` | `social_name` | `state_registration_rg` |
|---|---|---|---|---|
| Individual | CPF | Full name | Social name | RG |
| Legal entity | CNPJ | Legal name | Trade name | State registration |

The field names remain generic so the model can later support additional
countries and document systems.

## 5. Identification model

The initial implementation uses Brazilian documents:

```text
Individual    → CPF
Legal entity  → CNPJ
```

The model must be able to evolve toward:

```text
country
identification_type
identification
```

Document selection belongs to the document generator/provider capability, not
to customer or supplier generators.

### Identification uniqueness

`identification` is not the primary key, but it is a unique business key for
the clean dataset:

```text
Entity PK              → internal stable entity identifier
Entity identification → CPF or CNPJ, unique in the clean dataset
```

`generate_entity()` must not produce duplicate CPF/CNPJ values in a clean
scenario. The generator should use a generation context or registry to check
identifiers already issued during the current dataset run.

Duplicate identifiers must remain possible for ETL and data-quality exercises,
but only through an explicit anomaly or duplicate-injection mode. The default
golden dataset must never be silently duplicated.

## 6. Contact model

The base entity owns common contact information:

- `main_phone` is the primary landline or general phone;
- `main_mobile` is the primary mobile phone;
- `emails` supports multiple email addresses;
- `main_address` is the primary structured address.

The initial serialized representation for multiple emails is a semicolon-
separated string. The delimiter is `;`:

```text
email1@example.com;email2@example.com
```

This is an initial compatibility decision. A normalized email collection may be
introduced later without changing the ownership of the data.

## 7. Address model

`main_address` is a structured object, even while embedded in the entity:

```text
main_address
├── street
├── postal_code
├── city
├── state
├── district
└── country
```

The address may later be normalized into its own model or table. That future
normalization must preserve the entity-to-address relationship.

## 8. Generic capabilities

Each helper or generic generator must have one responsibility:

```text
generate_name()      → name values
generate_document()  → CPF, CNPJ, RG, or future document values
generate_email()     → email values
generate_phone()     → phone values
generate_address()   → structured address values
```

These capabilities must not contain customer or supplier business rules.

## 9. Provider model

The provider answers **how a value is obtained**. The generator answers **what
must be generated**.

The first provider is `FakerProvider`. Future providers may use geographic
datasets, databases, external APIs, or reference data, subject to the
Databricks Free Edition limitations documented in the project guidelines.

Provider contracts are capability-based:

```text
NameProvider
EmailProvider
AddressProvider
PhoneProvider
DocumentProvider
```

A single provider may implement multiple contracts:

```python
class FakerProvider(
    NameProvider,
    EmailProvider,
    AddressProvider,
    PhoneProvider,
    DocumentProvider,
):
    ...
```

Adding another provider must not require changes to entity, customer, or
supplier generators.

## 10. Layered architecture

```text
Domain generators
├── EntityGenerator
├── CustomerGenerator
└── SupplierGenerator
        ↓
Generic generators / capabilities
├── document
├── name
├── email
├── phone
└── address
        ↓
Provider contracts
        ↓
Provider implementations
└── FakerProvider
```

The dependency direction is one-way: domain generators depend on contracts,
and provider implementations satisfy those contracts. Domain generators must
not import `faker.Faker` directly.

## 11. Package layout

```text
src/mockerp/
├── providers/
│   ├── __init__.py
│   ├── provider_contract.py
│   └── faker_provider.py
├── generators/
│   ├── __init__.py
│   ├── entity.py
│   ├── customer.py
│   ├── supplier.py
│   ├── name.py
│   ├── document.py
│   ├── email.py
│   ├── phone.py
│   └── address.py
└── models/
    ├── __init__.py
    ├── entity.py
    └── address.py
```

The files listed for future generators and models are target structure, not a
claim that every file is already implemented.

## 12. Notebook boundary

Python package code is reusable and testable. Databricks notebooks are
execution and orchestration surfaces:

```text
notebook / Job
    ↓
domain generator
    ↓
generic capabilities
    ↓
provider implementation
```

Notebooks must not become the only place where entity-generation logic exists.

## 13. Non-negotiable invariants

- A specialization reuses an existing entity instead of recreating it.
- CPF/CNPJ is unique in the clean dataset, even though it is not the primary
  key.
- Duplicate CPF/CNPJ generation requires an explicit anomaly or test mode.
- Every `generate_*` function receives and propagates `config`.
- Clean mode preserves all normal guardrails.
- Dirty mode is opt-in and only relaxes explicitly configured rules.
- Customer generators do not generate supplier-specific fields.
- Supplier generators do not generate customer-specific fields.
- Generic helpers do not contain domain-specific rules.
- Providers do not contain customer or supplier business rules.
- The base entity owns common registration data.
- Country-specific document behavior is isolated behind document capability.
- The generator remains testable without a Databricks runtime.

## 14. Deferred scope

The following are intentionally not part of the first implementation:

- final customer-specific fields such as credit limit or payment terms;
- final supplier-specific fields such as category or supplier terms;
- multiple normalized phone records;
- normalized email and address tables;
- international document rules;
- external geographic or reference-data providers.

These items may be added through the roadmap, but must preserve the boundaries
defined in this SOT.
