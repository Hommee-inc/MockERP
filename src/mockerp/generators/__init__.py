"""Domain generators built on top of provider contracts."""

from .customer import CustomerGenerator, generate_customer

__all__ = ["CustomerGenerator", "generate_customer"]
