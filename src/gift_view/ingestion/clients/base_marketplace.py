from abc import abstractmethod
from typing import Dict, List, Tuple

from gift_view.ingestion.clients import BaseClient


class BaseMarketplaceClient(BaseClient):
    def __init__(
            self,
            base_url: str,
            max_retries: int = 5,
            retry_delay: int = 5,
            rate_limit_delay: int = 900,
            impersonate: str = "chrome136"
    ):
        super().__init__(
            base_url=base_url,
            max_retries=max_retries,
            retry_delay=retry_delay,
            rate_limit_delay=rate_limit_delay,
            impersonate=impersonate
        )


    @abstractmethod
    async def fetch_sales(self, state: Dict) -> List[Dict]:
        pass
