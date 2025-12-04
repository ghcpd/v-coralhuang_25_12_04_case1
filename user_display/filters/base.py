from abc import ABC, abstractmethod
from typing import Dict, Iterable, List


class UserFilter(ABC):
    @abstractmethod
    def match(self, user: Dict) -> bool:
        ...

    def filter(self, users: Iterable[Dict]) -> List[Dict]:
        return [u for u in users if self.match(u)]
