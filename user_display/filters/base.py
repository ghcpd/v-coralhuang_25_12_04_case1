from typing import Dict, Any, List


class Filter:
    def match(self, user: Dict[str, Any]) -> bool:
        raise NotImplementedError

    def filter(self, users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [u for u in users if self.match(u)]
