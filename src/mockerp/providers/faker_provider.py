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
    """Implement MockERP provider contracts with Faker."""

    def __init__(self, locale: str = "pt_BR", seed: int | None = None) -> None:
        self.fake = Faker(locale)
        if seed is not None:
            self.fake.seed_instance(seed)

    def name(self, name_type: str = "person") -> str:
        if name_type == "person":
            return self.fake.name()
        if name_type == "company":
            return self.fake.company()
        raise ValueError(f"Unsupported name type: {name_type}")

    def email(self, name: str | None = None) -> str:
        return self.fake.email() if name is None else self.fake.email(name=name)

    def address(self) -> dict[str, str]:
        return {
            "street": self.fake.street_name(),
            "postal_code": self.fake.postcode(),
            "city": self.fake.city(),
            "state": self.fake.estado_sigla(),
            "district": self.fake.bairro(),
            "country": self.fake.current_country(),
        }

    def phone(self) -> str:
        return self.fake.phone_number()

    def document(self, document_type: str) -> str:
        if document_type == "cpf":
            return self.fake.cpf()

        if document_type == "cnpj":
            return self.fake.cnpj()

        if document_type == "rg":
            return self.fake.numerify("##.###.###-#")

        if document_type == "state_registration":
            return self.fake.numerify("########-##")

        raise ValueError(f"Unsupported document type: {document_type}")
