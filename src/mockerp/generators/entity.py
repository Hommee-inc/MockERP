"""Base ERP entity generation."""

from collections.abc import MutableMapping

from mockerp.providers import FakerProvider, NameProvider

from .config import issued_identifications, validate_config

ENTITY_TYPES = {"individual", "legal_entity"}


def _unique_document(
    provider: FakerProvider,
    document_type: str,
    registry: set[str],
) -> str:
    for _ in range(100):
        document = provider.document(document_type)
        if document not in registry:
            registry.add(document)
            return document
    raise RuntimeError(f"Could not generate a unique {document_type}")


def _name(provider: NameProvider, entity_type: str) -> str:
    name_type = "company" if entity_type == "legal_entity" else "person"
    return provider.name(name_type)


def generate_entity(
    config: MutableMapping[str, object],
    entity_id: int,
    entity_type: str = "individual",
    *,
    provider: FakerProvider | None = None,
) -> dict[str, object]:
    """Generate one common registration record."""
    validate_config(config)
    if entity_id < 1:
        raise ValueError("entity_id must be greater than zero")
    if entity_type not in ENTITY_TYPES:
        raise ValueError("entity_type must be 'individual' or 'legal_entity'")

    locale = str(config.get("locale", "pt_BR"))
    seed = config.get("seed")
    faker_seed = seed if isinstance(seed, int) else None
    faker_provider = provider or FakerProvider(locale=locale, seed=faker_seed)

    document_type = "cpf" if entity_type == "individual" else "cnpj"
    registration_type = "rg" if entity_type == "individual" else "state_registration"
    address = faker_provider.address()
    name = _name(faker_provider, entity_type)

    return {
        "entity_id": entity_id,
        "entity_type": entity_type,
        "identification": _unique_document(
            faker_provider,
            document_type,
            issued_identifications(config),
        ),
        "name": name,
        "social_name": _name(faker_provider, entity_type),
        "main_phone": faker_provider.phone(),
        "main_mobile": faker_provider.phone(),
        "main_address": address,
        "emails": faker_provider.email(),
        "state_registration_rg": faker_provider.document(registration_type),
        "state_registration_issuer": address["state"],
    }
