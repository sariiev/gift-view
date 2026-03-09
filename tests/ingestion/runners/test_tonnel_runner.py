import pytest
from sqlalchemy import select

from gift_view.db.models.domain import Sale
from gift_view.db.resolvers import MarketplaceResolver, ModelResolver, GiftResolver, BackdropResolver, SymbolResolver, \
    AssetResolver
from gift_view.ingestion.parsers import TonnelParser
from gift_view.ingestion.runners import TonnelRunner


class FakeTonnelClient:
    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    async def fetch_sales(self, state):
        self.calls.append(state.copy())
        return self.responses.pop(0)


@pytest.mark.asyncio
async def test_runner_inserts_sales_and_updates_state(session_factory):
    fake_sales = [
        {
            "_id": "6998bf5832e4fa8a486bb35c",
            "gift_id": 9500985,
            "gift_num": 44572,
            "gift_name": "Spy Agaric",
            "bidder": 0,
            "price": 16,
            "timestamp": "2026-02-20T20:08:26.879Z",
            "model": "Rainbow Glow (0.5%)",
            "symbol": "Evil Pumpkin (1.5%)",
            "backdrop": "Satin Gold (2%)",
            "asset": "TON",
            "type": "SALE",
            "__v": 0
        }
    ]

    client = FakeTonnelClient(responses=[fake_sales])

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
        session_factory=session_factory
    )

    await runner.init()
    await runner.fetch_all()

    async with session_factory() as sess:
        res = await sess.execute(select(Sale))
        sales = res.scalars().all()

        assert len(sales) == 1
