from typing import Optional, Dict, List

from gift_view.ingestion.clients import BaseClient


class BinanceClient(BaseClient):
    def __init__(self):
        super().__init__(
            base_url="https://api.binance.com",
            max_retries=5,
            retry_delay=1,
            rate_limit_delay=300
        )


    async def get_klines(
            self,
            symbol: str,
            interval: str = "1h",
            start_time: Optional[int] = None,
            end_time: Optional[int] = None,
            limit: int = 1000
    ) -> List[Dict]:
        params = {
            "symbol": symbol.upper(),
            "interval": interval,
            "limit": limit
        }

        if start_time:
            params["startTime"] = start_time

        if end_time:
            params["endTime"] = end_time

        data = await self.get(
            path="/api/v3/klines",
            params=params
        )

        return data or []
