from typing import List, Dict, Any, Optional


class Formatter:
    def format(self, users: List[Dict[str, Any]], fields: Optional[List[str]] = None, **kwargs) -> str:
        raise NotImplementedError
