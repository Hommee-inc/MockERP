"""Shared configuration validation for MockERP generators."""

from collections.abc import MutableMapping

DATA_QUALITY_MODES = {"clean", "dirty"}


def validate_config(config: MutableMapping[str, object]) -> None:
    """Validate the shared generator configuration in place."""
    mode = config.get("data_quality_mode", "clean")
    if mode not in DATA_QUALITY_MODES:
        raise ValueError("data_quality_mode must be 'clean' or 'dirty'")


def issued_identifications(config: MutableMapping[str, object]) -> set[str]:
    """Return the run-local identification registry."""
    registry = config.setdefault("_issued_identifications", set())
    if not isinstance(registry, set):
        raise TypeError("config['_issued_identifications'] must be a set")
    return registry
