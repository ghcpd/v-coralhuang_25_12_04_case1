from typing import Dict, Any


class BaseValidator:
    def validate_and_recover(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """Return a recovered valid user dict or raise/return minimal fallback."""
        raise NotImplementedError()
