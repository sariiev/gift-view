from typing import Callable, AsyncContextManager, List, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.repositories import SaleRepository
from gift_view.db.repositories import MarketplaceStateRepository
from gift_view.db.resolvers import MarketplaceResolver
from gift_view.ingestion.clients import TonnelClient
from gift_view.ingestion.parsers import TonnelParser
from gift_view.ingestion.runners import BaseMarketplaceRunner


class TonnelRunner(BaseMarketplaceRunner):
    def __init__(
            self,
            marketplace_client: TonnelClient,
            marketplace_parser: TonnelParser,
            session_factory: Callable[[], AsyncContextManager[AsyncSession]]
    ):
        super().__init__(
            marketplace_client=marketplace_client,
            marketplace_parser=marketplace_parser,
            session_factory=session_factory
        )


    async def init(self):
        async with self.session_factory() as session:
            marketplace_resolver = MarketplaceResolver()
            self.marketplace_id = await marketplace_resolver.resolve_id(session=session, name="Tonnel")


    async def run_once(self):
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

            raw_sales = await self.marketplace_client.fetch_sales(state=state)
            await self.process_batch(
                session=session,
                raw_sales=raw_sales
            )

            if len(raw_sales) < state["limit"]:
                return
            state["page"] += 1
            await marketplace_state_repository.upsert(
                marketplace_id=self.marketplace_id,
                state=state
            )

    async def process_batch(self, session: AsyncSession, raw_sales: List[Dict]):
        parsed_sales = await self.marketplace_parser.parse_sales(session=session, sales=raw_sales)
        sale_repository = SaleRepository(session=session)
        await sale_repository.add_all(sales=parsed_sales)
