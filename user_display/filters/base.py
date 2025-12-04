from typing import Dict, Any


class BaseFilter:
    """Base filter interface.

    Implement a callable that accepts (user, criteria) and returns bool.
    """

    def matches(self, user: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        raise NotImplementedError()
