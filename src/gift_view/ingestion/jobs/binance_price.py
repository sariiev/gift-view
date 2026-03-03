import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from gift_view.config import setup_logging
from gift_view.db.session import get_session
from gift_view.ingestion.clients import BinanceClient
from gift_view.ingestion.parsers import BinancePriceParser
from gift_view.ingestion.runners import BinanceRunner
from gift_view.scheduler import build_trigger


setup_logging()


class BinancePriceJob:
    def __init__(
            self,
            runner: BinanceRunner,
            interval: int
    ):
        self.runner = runner
        self.interval = interval
        self.scheduler = AsyncIOScheduler(timezone="UTC")


    async def main(self):
        self.scheduler.add_job(
            self.runner.run_once,
            trigger=build_trigger(interval=self.interval),
            id="binance_runner",
            max_instances=1,
            coalesce=True
        )

        await self.runner.run_once()

        self.scheduler.start()

        try:
            await asyncio.Event().wait()
        finally:
            self.scheduler.shutdown()


if __name__ == '__main__':
    client = BinanceClient()
    parser = BinancePriceParser()
    runner = BinanceRunner(
        client=client,
        parser=parser,
        session_factory=get_session,
        interval=3600
    )
    job = BinancePriceJob(runner, 3600)
    asyncio.run(job.main())
