from .base import Validator
from .default import DefaultValidator
from ..plugins import register_validator

register_validator("default", lambda **kwargs: DefaultValidator(**kwargs))

__all__ = ["Validator", "DefaultValidator"]
