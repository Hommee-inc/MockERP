"""Contracts implemented by providers used by MockERP generators."""

from abc import ABC, abstractmethod


class NameProvider(ABC):
    """Provide person or company names."""

    @abstractmethod
    def name(self) -> str:
        """Return a generated name."""


class EmailProvider(ABC):
    """Provide email addresses."""

    @abstractmethod
    def email(self, name: str | None = None) -> str:
        """Return a generated email address."""


class AddressProvider(ABC):
    """Provide postal addresses."""

    @abstractmethod
    def address(self) -> dict[str, str | None]:
        """Return a normalized address."""


class PhoneProvider(ABC):
    """Provide phone numbers."""

    @abstractmethod
    def phone(self) -> str:
        """Return a generated phone number."""


class DocumentProvider(ABC):
    """Provide Brazilian identity and tax documents."""

    @abstractmethod
    def cpf(self) -> str:
        """Return a generated CPF."""

    @abstractmethod
    def cnpj(self) -> str:
        """Return a generated CNPJ."""
