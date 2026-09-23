# """Provider interfaces and concrete data providers."""

from .faker_provider import FakerProvider
from .provider_contract import (
    AddressProvider,
    DocumentProvider,
    EmailProvider,
    NameProvider,
    PhoneProvider,
)

__all__ = [
    "AddressProvider",
    "DocumentProvider",
    "EmailProvider",
    "FakerProvider",
    "NameProvider",
    "PhoneProvider",
]
