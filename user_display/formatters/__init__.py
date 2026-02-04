from .compact import CompactFormatter
from .json_fmt import JsonFormatter
from .table import TableFormatter
from ..plugins import register_formatter

# Register built-in formatters
register_formatter("compact", lambda **kwargs: CompactFormatter(**kwargs))
register_formatter("json", lambda **kwargs: JsonFormatter(**kwargs))
register_formatter("table", lambda **kwargs: TableFormatter(**kwargs))

__all__ = ["CompactFormatter", "JsonFormatter", "TableFormatter"]
