"""Domain generators built on top of provider contracts."""

from .customer import CustomerGenerator, generate_customer
from .entity import generate_entity

__all__ = ["CustomerGenerator", "generate_customer", "generate_entity"]
