from mockerp.generators import generate_entity


def clean_config(seed: int = 7) -> dict[str, object]:
    return {
        "locale": "pt_BR",
        "seed": seed,
        "data_quality_mode": "clean",
    }


def test_entity_has_the_base_registration_schema() -> None:
    entity = generate_entity(clean_config(), 1)

    assert set(entity) == {
        "entity_id",
        "entity_type",
        "identification",
        "name",
        "social_name",
        "main_phone",
        "main_mobile",
        "main_address",
        "emails",
        "state_registration_rg",
        "state_registration_issuer",
    }
    assert set(entity["main_address"]) == {
        "street",
        "postal_code",
        "city",
        "state",
        "district",
        "country",
    }


def test_entity_supports_individual_and_legal_entity_documents() -> None:
    config = clean_config()
    individual = generate_entity(config, 1, "individual")
    company = generate_entity(config, 2, "legal_entity")

    assert len(individual["identification"]) == 14
    assert len(company["identification"]) == 18
    assert individual["entity_type"] == "individual"
    assert company["entity_type"] == "legal_entity"


def test_clean_generation_keeps_identifications_unique() -> None:
    config = clean_config()
    entities = [generate_entity(config, entity_id) for entity_id in range(1, 21)]

    identifications = [entity["identification"] for entity in entities]
    assert len(identifications) == len(set(identifications))


def test_same_seed_reproduces_the_first_entity() -> None:
    first = generate_entity(clean_config(42), 1)
    second = generate_entity(clean_config(42), 1)

    assert first == second
