"""Customer generation for the MockERP commercial core."""

from __future__ import annotations

import random
from collections.abc import Callable
from datetime import datetime, timezone

from mockerp.providers import (
    AddressProvider,
    DocumentProvider,
    EmailProvider,
    FakerProvider,
    NameProvider,
)


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

    def generate(self, customer_id: int) -> dict[str, object]:
        """Generate one customer record with a stable ERP-shaped schema."""
        if customer_id < 1:
            raise ValueError("customer_id must be greater than zero")

        name = self._name_provider.name()
        address = self._address_provider.address()

        return {
            "customer_id": customer_id,
            "name": name,
            "document": self._document_provider.cpf(),
            "email": self._email_provider.email(name),
            "city": address["city"],
            "state": address["state"],
            "created_at": self._clock(),
            "status": self._rng.choice(("ACTIVE", "INACTIVE")),
        }


def generate_customer(
    customer_id: int,
    *,
    provider: FakerProvider | None = None,
    seed: int | None = None,
) -> dict[str, object]:
    """Generate one customer using the default Brazilian Faker provider."""
    faker_provider = provider or FakerProvider(seed=seed)
    generator = CustomerGenerator(
        faker_provider,
        faker_provider,
        faker_provider,
        faker_provider,
        rng=random.Random(seed),
    )
    return generator.generate(customer_id)
