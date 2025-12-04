from .base import BaseValidator
from typing import Dict, Any
from . import base
from ..metrics import GLOBAL as METRICS


class DefaultValidator(BaseValidator):
    """Basic field validation with soft recovery and defaults.

    The validator attempts to ensure minimal fields exist and types are safe.
    """

    DEFAULTS = {
        "id": None,
        "name": "",
        "email": "",
        "role": "User",
        "status": "Inactive",
        "join_date": "1970-01-01",
        "last_login": "1970-01-01",
    }

    def validate_and_recover(self, user: Dict[str, Any]) -> Dict[str, Any]:
        out = {}
        for k, dv in self.DEFAULTS.items():
            v = user.get(k, dv)
            if k == "id":
                # try to coerce ints safely
                try:
                    if v is None:
                        out["id"] = None
                    else:
                        out["id"] = int(v)
                except Exception:
                    METRICS.incr("validation_failures")
                    out["id"] = None
            else:
                out[k] = v if v is not None else dv

        # keep any additional fields
        for k, v in user.items():
            if k not in out:
                out[k] = v

        return out
