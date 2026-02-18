import asyncio
import time
from datetime import datetime, timezone, timedelta
from typing import Callable, AsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.repositories import AssetRepository, AssetPriceRepository
from gift_view.ingestion.clients import BinanceClient
from gift_view.ingestion.parsers import BinancePriceParser


class BinanceRunner:
    def __init__(
            self,
            client: BinanceClient,
            parser: BinancePriceParser,
            session_factory: Callable[[], AsyncContextManager[AsyncSession]],
            interval: int = 3600,
            delay: int = 1
    ):
        self.client = client
        self.parser = parser
        self.session_factory = session_factory
        self.interval = interval
        self.interval_str = self.to_interval_str(interval=self.interval)
        self.delay = delay


    async def run_once(self):
        async with self.session_factory() as session:
            asset_repository = AssetRepository(session)
            asset_price_repository = AssetPriceRepository(session)

            assets = await asset_repository.get_all()
            for asset in assets:
                latest_timestamp = await asset_price_repository.get_latest_timestamp(asset)

                if latest_timestamp is None:
                    start = datetime(2025, 1, 1, tzinfo=timezone.utc)
                else:
                    start = latest_timestamp + timedelta(seconds=self.interval)

                now = datetime.now(tz=timezone.utc)
                while start < now:
                    request_start = time.monotonic()
                    klines = await self.client.get_klines(
                        symbol=f"{asset.symbol}USDT",
                        interval=self.interval_str,
                        start_time=int(start.timestamp() * 1000)
                    )


                    prices = self.parser.parse_klines(
                        klines=klines,
                        asset_id=asset.id
                    )

                    asset_price_repository.add_all(asset_prices=prices)

                    if not prices:
                        break
                    last_timestamp = prices[-1].timestamp
                    start = last_timestamp + timedelta(seconds=self.interval)

                    request_end = time.monotonic()
                    passed = request_end - request_start
                    if passed < self.delay:
                        await asyncio.sleep(self.delay - passed)


    INTERVAL_MAP = {
        1: "1s",
        60: "1m",
        60 * 3: "3m",
        60 * 5: "5m",
        60 * 15: "15m",
        60 * 30: "30m",
        60 * 60: "1h",
        60 * 60 * 2: "2h",
        60 * 60 * 4: "4h",
        60 * 60 * 6: "6h",
        60 * 60 * 8: "8h",
        60 * 60 * 12: "12h",
        60 * 60 * 24: "1d",
        60 * 60 * 24 * 3: "3d",
        60 * 60 * 24 * 7: "1w",
    }

    def to_interval_str(self, interval: int) -> str:
        try:
            return self.INTERVAL_MAP[interval]
        except KeyError:
            raise ValueError(f"Unsupported interval: {interval}")
