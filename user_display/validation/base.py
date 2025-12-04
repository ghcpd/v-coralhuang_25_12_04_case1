from typing import Dict, Any


class Validator:
    def validate(self, user: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
