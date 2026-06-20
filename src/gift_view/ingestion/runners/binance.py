import asyncio
import time
from datetime import datetime, timezone, timedelta
from logging import getLogger
from typing import Callable, AsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.repositories.domain import AssetRepository, AssetPriceRepository
from gift_view.ingestion.clients import BinanceClient
from gift_view.ingestion.parsers import BinancePriceParser
from gift_view.utils import to_interval_seconds


BINANCE_ASSETS = {"TON"}

class BinanceRunner:
    def __init__(
            self,
            client: BinanceClient,
            parser: BinancePriceParser,
            session_factory: Callable[[], AsyncContextManager[AsyncSession]],
            interval: str = "1h",
            delay: int = 1
    ):
        self.client = client
        self.parser = parser
        self.session_factory = session_factory
        self.interval = interval
        self.interval_seconds = to_interval_seconds(interval=interval)
        self.delay = delay
        self.logger = getLogger(self.__class__.__name__)


    async def run_once(self):
        self.logger.info("Binance run triggered")
        async with self.session_factory() as session:
            asset_repository = AssetRepository(session)
            asset_price_repository = AssetPriceRepository(session)

            assets = await asset_repository.get_all()
            assets = [a for a in assets if a.symbol in BINANCE_ASSETS]
            for asset in assets:
                latest_timestamp = await asset_price_repository.get_latest_timestamp(asset.id)

                if latest_timestamp is None:
                    start = datetime(2025, 1, 1, tzinfo=timezone.utc)
                else:
                    start = latest_timestamp + timedelta(seconds=self.interval_seconds)

                now = datetime.now(tz=timezone.utc)
                while start < now:
                    request_start = time.monotonic()
                    self.logger.info("Fetching %sUSDT klines (start_time=%s)", asset.symbol, start)
                    klines = await self.client.get_klines(
                        symbol=f"{asset.symbol}USDT",
                        interval=self.interval,
                        start_time=int(start.timestamp() * 1000)
                    )
                    self.logger.info("Fetched %s %sUSDT klines", len(klines), asset.symbol)


                    prices = self.parser.parse_klines(
                        klines=klines,
                        asset_id=asset.id
                    )

                    asset_price_repository.add_all(asset_prices=prices)

                    if not prices:
                        break
                    last_timestamp = prices[-1].timestamp
                    start = last_timestamp + timedelta(seconds=self.interval_seconds)

                    request_end = time.monotonic()
                    passed = request_end - request_start
                    if passed < self.delay:
                        await asyncio.sleep(self.delay - passed)
