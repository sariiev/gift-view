import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from gift_view.config import load_tonnel_config
from gift_view.db.resolvers import MarketplaceResolver, GiftResolver, ModelResolver, BackdropResolver, SymbolResolver, \
    AssetResolver
from gift_view.db.session import get_session
from gift_view.ingestion.clients import TonnelClient
from gift_view.ingestion.parsers import TonnelParser
from gift_view.ingestion.runners import TonnelRunner
from gift_view.scheduler import build_trigger


class TonnelSalesJob:
    def __init__(
            self,
            runner: TonnelRunner,
            interval: int
    ):
        self.runner = runner
        self.interval = interval
        self.scheduler = AsyncIOScheduler(timezone="UTC")


    async def main(self):
        self.scheduler.add_job(
            self.runner.run_once,
            trigger=build_trigger(interval=self.interval),
            id="tonnel_runner",
            max_instances=1,
            coalesce=True
        )

        await self.runner.init()
        await self.runner.run_once()

        self.scheduler.start()

        try:
            await asyncio.Event().wait()
        finally:
            self.scheduler.shutdown()

if __name__ == '__main__':
    client = TonnelClient(
        config=load_tonnel_config()
    )
    parser = TonnelParser(
        marketplace_resolver=MarketplaceResolver(),
        gift_resolver=GiftResolver(),
        model_resolver=ModelResolver(),
        backdrop_resolver=BackdropResolver(),
        symbol_resolver=SymbolResolver(),
        asset_resolver=AssetResolver()
    )
    runner = TonnelRunner(
        marketplace_client=client,
        marketplace_parser=parser,
        session_factory=get_session
    )
    job = TonnelSalesJob(
        runner=runner,
        interval=60
    )
    asyncio.run(job.main())
