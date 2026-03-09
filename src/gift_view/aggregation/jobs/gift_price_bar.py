import asyncio
from typing import List

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from gift_view.aggregation.aggregators import GiftPriceBarAggregator
from gift_view.config import setup_logging
from gift_view.db.session import get_session
from gift_view.scheduler import build_trigger
from gift_view.utils import to_interval_seconds


setup_logging()


class GiftPriceBarAggregationJob:
    def __init__(
            self,
            aggregator: GiftPriceBarAggregator,
            intervals: List[str]
    ):
        self.aggregator = aggregator
        self.intervals = intervals or ["1h", "4h", "1d", "1w"]
        intervals_seconds = [to_interval_seconds(interval=interval) for interval in self.intervals]
        self.interval_seconds = min(intervals_seconds)
        self.scheduler = AsyncIOScheduler(timezone="UTC")


    async def main(self):
        self.scheduler.add_job(
            self.aggregator.aggregate_all,
            trigger=build_trigger(interval=self.interval_seconds),
            id="gift_price_bar_aggregator",
            max_instances=1,
            coalesce=True
        )

        await self.aggregator.aggregate_all()

        self.scheduler.start()

        try:
            await asyncio.Event().wait()
        finally:
            self.scheduler.shutdown()


if __name__ == '__main__':
    intervals = ["1h", "4h", "1d", "1w"]
    aggregator = GiftPriceBarAggregator(
        session_factory=get_session,
        intervals=intervals
    )
    job = GiftPriceBarAggregationJob(
        aggregator=aggregator,
        intervals=intervals
    )
    asyncio.run(job.main())
