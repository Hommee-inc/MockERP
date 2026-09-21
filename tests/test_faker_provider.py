from mockerp.providers import FakerProvider


def test_faker_provider_implements_brazilian_provider_contracts() -> None:
    provider = FakerProvider(seed=7)

    assert provider.name()
    assert "@" in provider.email()
    assert provider.phone()
    assert len(provider.document("cpf")) == 14
    assert len(provider.document("cnpj")) == 18
    assert provider.address()


def test_faker_provider_rejects_unsupported_document_types() -> None:
    provider = FakerProvider(seed=7)

    import pytest

    with pytest.raises(ValueError, match="Unsupported document type"):
        provider.document("passport")
