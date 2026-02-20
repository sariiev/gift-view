from typing import Dict, List

from gift_view.config import TonnelConfig
from gift_view.ingestion.clients import BaseMarketplaceClient, BaseClient


class TonnelClient(BaseMarketplaceClient):
    def __init__(self, http_client: BaseClient, config: TonnelConfig):
        self.http_client = http_client
        self.config = config

    async def fetch_sales(self, state: Dict) -> List[Dict]:
        page = state.get("page", 1)
        limit = state.get("limit", 50)

        return await self.http_client.post(
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
