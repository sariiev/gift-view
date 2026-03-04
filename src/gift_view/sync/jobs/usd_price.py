import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from gift_view.config import setup_logging
from gift_view.db.session import get_session
from gift_view.scheduler import build_trigger
from gift_view.sync.syncers import UsdPriceSyncer


setup_logging()


class UsdPriceJob:
    def __init__(
            self,
            syncer: UsdPriceSyncer,
            interval: int
    ):
        self.syncer = syncer
        self.interval = interval
        self.scheduler = AsyncIOScheduler(timezone="UTC")


    async def main(self):
        self.scheduler.add_job(
            self.syncer.sync_all,
            trigger=build_trigger(interval=self.interval),
            id="usd_price_syncer",
            max_instances=1,
            coalesce=True
        )

        await self.syncer.sync_all()

        self.scheduler.start()

        try:
            await asyncio.Event().wait()
        finally:
            self.scheduler.shutdown()


if __name__ == '__main__':
    syncer = UsdPriceSyncer(
        session_factory=get_session,
        interval=3600,
        batch_size=500
    )
    job = UsdPriceJob(
        syncer=syncer,
        interval=60
    )
    asyncio.run(job.main())
