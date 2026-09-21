"""Customer generation for the MockERP commercial core."""

from __future__ import annotations

import random
from collections.abc import Callable, MutableMapping
from datetime import datetime, timezone

from mockerp.providers import (
    AddressProvider,
    DocumentProvider,
    EmailProvider,
    FakerProvider,
    NameProvider,
)

from .config import validate_config


class CustomerGenerator:
    """Generate customers from injectable provider contracts.

    The generator owns business-shape decisions, while providers own the
    production of individual fake values. This keeps the domain generator
    independent from Faker and makes providers replaceable in tests or jobs.
    """

    def __init__(
        self,
        name_provider: NameProvider,
        email_provider: EmailProvider,
        address_provider: AddressProvider,
        document_provider: DocumentProvider,
        *,
        rng: random.Random | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._name_provider = name_provider
        self._email_provider = email_provider
        self._address_provider = address_provider
        self._document_provider = document_provider
        self._rng = rng or random.Random()
        self._clock = clock or (lambda: datetime.now(timezone.utc))

    def generate(
        self,
        config: MutableMapping[str, object],
        customer_id: int,
    ) -> dict[str, object]:
        """Generate one customer record with a stable ERP-shaped schema."""
        if customer_id < 1:
            raise ValueError("customer_id must be greater than zero")

        validate_config(config)

        name = self._name_provider.name()
        address = self._address_provider.address()

        return {
            "customer_id": customer_id,
            "name": name,
            "document": self._document_provider.document("cpf"),
            "email": self._email_provider.email(name),
            "address": address,
            "created_at": self._clock(),
            "status": self._rng.choice(("ACTIVE", "INACTIVE")),
        }


def generate_customer(
    config: MutableMapping[str, object],
    customer_id: int,
    *,
    provider: FakerProvider | None = None,
) -> dict[str, object]:
    """Generate one customer using the configuration object."""
    locale = str(config.get("locale", "pt_BR"))
    seed = config.get("seed")
    faker_seed = seed if isinstance(seed, int) else None
    faker_provider = provider or FakerProvider(locale=locale, seed=faker_seed)
    generator = CustomerGenerator(
        faker_provider,
        faker_provider,
        faker_provider,
        faker_provider,
        rng=random.Random(faker_seed),
    )
    return generator.generate(config, customer_id)
