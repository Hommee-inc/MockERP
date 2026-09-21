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

    customer = generator.generate({"data_quality_mode": "clean"}, 1)

    assert set(customer) == {
        "customer_id",
        "name",
        "document",
        "email",
        "address",
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
        generator.generate({"data_quality_mode": "clean"}, 0)


def test_customer_generator_rejects_unknown_data_quality_mode() -> None:
    provider = FakerProvider(seed=7)
    generator = CustomerGenerator(provider, provider, provider, provider)

    with pytest.raises(ValueError, match="data_quality_mode"):
        generator.generate({"data_quality_mode": "unknown"}, 1)
