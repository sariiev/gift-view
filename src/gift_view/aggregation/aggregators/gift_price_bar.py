from datetime import datetime, timezone

from gift_view.aggregation.aggregators.base_aggregator import BaseAggregator
from gift_view.db.repositories.aggregation import GiftPriceBarRepository


class GiftPriceBarAggregator(BaseAggregator):
    async def aggregate_all(self):
        self.logger.info("Gift price bar aggregation triggered")
        async with self.session_factory() as session:
            gift_price_bar_repository = GiftPriceBarRepository(session=session)
            for interval in self.intervals:
                start = await gift_price_bar_repository.get_latest_timestamp(interval=interval)

                if start is None:
                    start = datetime(2025, 1, 1, tzinfo=timezone.utc)
                else:
                    start -= self.interval_delta(interval=interval)

                self.logger.info("Aggregating gift sales for %s interval from %s", interval, start)
                await gift_price_bar_repository.aggregate(start=start, interval=interval)
                self.logger.info("Aggregated gift sales for %s interval (start=%s)", interval, start)