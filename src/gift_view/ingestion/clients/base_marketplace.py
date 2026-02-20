from abc import ABC, abstractmethod
from typing import Dict, List, Tuple


class BaseMarketplaceClient(ABC):
    @abstractmethod
    async def fetch_sales(self, state: Dict) -> Tuple[List[Dict], Dict]:
        pass
