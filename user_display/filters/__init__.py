from .base import UserFilter
from .regex_filter import RegexFilter
from .composite_filter import CompositeFilter
from ..plugins import register_filter

register_filter("regex", lambda **kwargs: RegexFilter(**kwargs))
register_filter("composite", lambda **kwargs: CompositeFilter(**kwargs))

__all__ = ["UserFilter", "RegexFilter", "CompositeFilter"]
