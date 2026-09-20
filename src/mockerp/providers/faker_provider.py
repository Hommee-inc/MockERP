"""Faker-backed provider implementation for Brazilian mock data."""

from faker import Faker

from .provider_contract import (
    AddressProvider,
    DocumentProvider,
    EmailProvider,
    NameProvider,
    PhoneProvider,
)


class FakerProvider(
    NameProvider,
    EmailProvider,
    AddressProvider,
    PhoneProvider,
    DocumentProvider,
):
    """Implement MockERP provider contracts with Faker's Brazilian locale."""

    def __init__(self, seed: int | None = None) -> None:
        self._faker = Faker("pt_BR")
        if seed is not None:
            self._faker.seed_instance(seed)

    def name(self) -> str:
        return self._faker.name()

    def email(self, name: str | None = None) -> str:
        return self._faker.email() if name is None else self._faker.email(name=name)

    def address(self) -> dict[str, str | None]:
        return {
            "street": self._faker.street_name(),
            "number": self._faker.building_number(),
            "neighborhood": self._faker.bairro(),
            "city": self._faker.city(),
            "state": self._faker.estado_sigla(),
            "postal_code": self._faker.postcode(),
        }

    def phone(self) -> str:
        return self._faker.phone_number()

    def cpf(self) -> str:
        return self._faker.cpf()

    def cnpj(self) -> str:
        return self._faker.cnpj()
