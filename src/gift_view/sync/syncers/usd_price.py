from datetime import datetime
from logging import getLogger
from typing import Callable, AsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.repositories.domain import SaleRepository, AssetPriceRepository


class UsdPriceSyncer:
    def __init__(
            self,
            session_factory: Callable[[], AsyncContextManager[AsyncSession]],
            interval: int,
            batch_size: int = 500
    ):
        self.session_factory = session_factory
        self.interval = interval
        self.batch_size = batch_size
        self.logger = getLogger(self.__class__.__name__)


    async def sync_all(self):
        self.logger.info("USD price sync triggered")
        while True:
            has_unsynced = await self.sync_batch()
            if not has_unsynced:
                break


    async def sync_batch(self):
        async with self.session_factory() as session:
            sale_repository = SaleRepository(session=session)
            asset_price_repository = AssetPriceRepository(session=session)

            self.logger.info("Fetching unsynced sales (batch_size=%s)", self.batch_size)
            sales = await sale_repository.get_without_usd_price(limit=self.batch_size)
            self.logger.info("Fetched %s unsynced sales", len(sales))

            if not sales:
                return False

            lookup = {}
            for sale in sales:
                rounded_timestamp = self.round_timestamp(timestamp=sale.timestamp)
                lookup[(sale.asset_id, rounded_timestamp)] = None

            prices = await asset_price_repository.get_at_timestamps(keys=list(lookup.keys()))

            prices_map = {
                (price.asset_id, price.timestamp) : price.price_usd
                for price in prices
            }

            updated = 0
            for sale in sales:
                rounded_timestamp = self.round_timestamp(timestamp=sale.timestamp)

                key = (sale.asset_id, rounded_timestamp)

                if key in prices_map:
                    updated += 1
                    sale.price_usd = sale.price_native * prices_map[key]
            self.logger.info("Synced USD price for %s sales", updated)

            return len(sales) == self.batch_size


    def round_timestamp(self, timestamp: datetime) -> datetime:
        seconds = int(self.interval)
        epoch = int(timestamp.timestamp())
        rounded = epoch - (epoch % seconds)
        return datetime.fromtimestamp(rounded, tz=timestamp.tzinfo)
