from mockerp.providers import FakerProvider


def test_faker_provider_implements_brazilian_provider_contracts() -> None:
    provider = FakerProvider(seed=7)

    assert provider.name()
    assert "@" in provider.email()
    assert provider.phone()
    assert len(provider.cpf()) == 14
    assert len(provider.cnpj()) == 18

    address = provider.address()
    assert {
        "street",
        "number",
        "neighborhood",
        "city",
        "state",
        "postal_code",
    } == set(address)
