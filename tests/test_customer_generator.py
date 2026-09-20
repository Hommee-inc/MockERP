from datetime import datetime, timezone

import pytest

from mockerp.generators import CustomerGenerator
from mockerp.providers import FakerProvider


def test_customer_generator_returns_v01_customer_schema() -> None:
    provider = FakerProvider(seed=7)
    created_at = datetime(2026, 1, 1, tzinfo=timezone.utc)
    generator = CustomerGenerator(
        provider,
        provider,
        provider,
        provider,
        clock=lambda: created_at,
    )

    customer = generator.generate(1)

    assert set(customer) == {
        "customer_id",
        "name",
        "document",
        "email",
        "city",
        "state",
        "created_at",
        "status",
    }
    assert customer["customer_id"] == 1
    assert customer["created_at"] == created_at
    assert customer["status"] in {"ACTIVE", "INACTIVE"}
    assert "@" in customer["email"]


def test_customer_id_must_be_positive() -> None:
    provider = FakerProvider(seed=7)
    generator = CustomerGenerator(provider, provider, provider, provider)

    with pytest.raises(ValueError, match="greater than zero"):
        generator.generate(0)
