from typing import Dict, List

from gift_view.config import TonnelConfig
from gift_view.ingestion.clients import BaseMarketplaceClient, BaseClient


class TonnelClient(BaseMarketplaceClient):
    def __init__(self,
                 config: TonnelConfig,
                 max_retries: int = 5,
                 retry_delay: int = 5,
                 rate_limit_delay: int = 900,
                 impersonate: str = "chrome136",
    ):
        super().__init__(
            base_url="https://gifts2.tonnel.network/api",
            max_retries=max_retries,
            retry_delay=retry_delay,
            rate_limit_delay=rate_limit_delay,
            impersonate=impersonate
        )
        self.config = config


    async def fetch_sales(self, state: Dict) -> List[Dict]:
        page = state.get("page", 1)
        limit = state.get("limit", 50)

        return await self.post(
            path="/saleHistory",
            json= {
                "authData": self.config.auth_data,
                "limit": limit,
                "page": page,
                "sort": {
                    "timestamp": 1
                },
                "type": ["SALE", "INTERNAL_SALE"]
            },
            timeout=10
        )
