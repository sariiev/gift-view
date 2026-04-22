import asyncio
import time
from logging import getLogger
from typing import Callable, AsyncContextManager, List, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.repositories.domain import SaleRepository
from gift_view.db.repositories.domain import MarketplaceStateRepository
from gift_view.db.resolvers import MarketplaceResolver
from gift_view.ingestion.clients import TonnelClient
from gift_view.ingestion.parsers import TonnelParser
from gift_view.ingestion.runners import BaseMarketplaceRunner


class TonnelRunner(BaseMarketplaceRunner):
    def __init__(
            self,
            marketplace_client: TonnelClient,
            marketplace_parser: TonnelParser,
            session_factory: Callable[[], AsyncContextManager[AsyncSession]],
            delay: int = 3
    ):
        super().__init__(
            marketplace_client=marketplace_client,
            marketplace_parser=marketplace_parser,
            session_factory=session_factory,
            delay=delay
        )
        self.logger = getLogger(self.__class__.__name__)


    async def init(self):
        async with self.session_factory() as session:
            marketplace_resolver = MarketplaceResolver()
            self.marketplace_id = await marketplace_resolver.resolve_id(session=session, name="Tonnel", create=True)
        self.logger.info("Tonnel runner init")


    async def fetch_all(self):
        self.logger.info("Tonnel run triggered")
        while True:
            fetch_start = time.monotonic()
            has_next = await self.fetch_once()
            if not has_next:
                break
            fetch_end = time.monotonic()
            passed = fetch_end - fetch_start
            if passed < self.delay:
                await asyncio.sleep(self.delay - passed)


    async def fetch_once(self) -> bool:
        async with self.session_factory() as session:
            marketplace_state_repository = MarketplaceStateRepository(session=session)
            marketplace_state = await marketplace_state_repository.get_by_marketplace_id(
                marketplace_id=self.marketplace_id)
            if marketplace_state is None:
                state = {
                    "page": 1,
                    "limit": 50
                }
            else:
                state = marketplace_state.state

            self.logger.info("Fetching page %s (limit %s)", state["page"], state["limit"])
            raw_sales = await self.marketplace_client.fetch_sales(state=state)
            self.logger.info("Fetched %s sales", len(raw_sales))
            await self.process_batch(
                session=session,
                raw_sales=raw_sales
            )

            if len(raw_sales) < state["limit"]:
                self.logger.info("Page is not full, pausing fetching")
                return False

            self.logger.info("Advancing to next page %s", state["page"] + 1)
            await marketplace_state_repository.upsert(
                marketplace_id=self.marketplace_id,
                state={**state, "page": state["page"] + 1}
            )
            return True


    async def process_batch(self, session: AsyncSession, raw_sales: List[Dict]):
        parsed_sales = await self.marketplace_parser.parse_sales(session=session, sales=raw_sales)
        sale_repository = SaleRepository(session=session)
        await sale_repository.add_all(sales=parsed_sales)
