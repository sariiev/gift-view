from datetime import timedelta, datetime, timezone
from logging import getLogger
from typing import Callable, AsyncContextManager, List

from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.repositories.aggregation import GiftPriceBarRepository


class GiftPriceBarAggregator:
    def __init__(
            self,
            session_factory: Callable[[], AsyncContextManager[AsyncSession]],
            intervals: List[str]
    ):
        self.session_factory = session_factory
        self.intervals = intervals or ["1h", "4h", "1d", "1w"]
        self.logger = getLogger(self.__class__.__name__)


    async def aggregate_all(self):
        self.logger.info("Gift price bar aggregation triggered")
        async with self.session_factory() as session:
            gift_price_bar_repository = GiftPriceBarRepository(session=session)
            for interval in self.intervals:
                self.logger.info("Aggregating gift sales for %s interval", interval)
                start = await gift_price_bar_repository.get_latest_timestamp(interval=interval)

                if start is None:
                    start = datetime(2025, 1, 1, tzinfo=timezone.utc)
                else:
                    start -= timedelta(hours=1)

                await gift_price_bar_repository.aggregate(start=start, interval=interval)
                self.logger.info("Aggregated gift sales for %s interval", interval)


    def interval_delta(self, interval: str) -> timedelta:
        if interval == "1h":
            return timedelta(hours=1)
        if interval == "4h":
            return timedelta(hours=4)
        if interval == "1d":
            return timedelta(days=1)
        if interval == "1w":
            return timedelta(weeks=1)
        raise ValueError(f"Unsupported interval: {interval}")
