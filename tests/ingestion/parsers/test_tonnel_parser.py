from datetime import datetime, timezone

import pytest

from gift_view.db.resolvers import MarketplaceResolver, GiftResolver, ModelResolver, BackdropResolver, SymbolResolver, \
    AssetResolver
from gift_view.ingestion.parsers import TonnelParser


@pytest.mark.asyncio
async def test_parse_single_sale(session):
    parser = TonnelParser(
        marketplace_resolver=MarketplaceResolver(),
        gift_resolver=GiftResolver(),
        model_resolver=ModelResolver(),
        backdrop_resolver=BackdropResolver(),
        symbol_resolver=SymbolResolver(),
        asset_resolver=AssetResolver()
    )

    raw_sales = [
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

    parsed_sales = await parser.parse_sales(session=session, sales=raw_sales)

    assert len(parsed_sales) == 1

    sale = parsed_sales[0]

    assert sale.marketplace_sale_id == "6998bf5832e4fa8a486bb35c"
    assert sale.gift_id is not None
    assert sale.gift_number == 44572
    assert sale.model_id is not None
    assert sale.backdrop_id is not None
    assert sale.symbol_id is not None
    assert sale.asset_id is not None
    assert sale.price_native == 16
    assert sale.price_usd is None
    assert sale.timestamp == datetime(
        2026, 2, 20, 20, 8, 26, 879000, tzinfo=timezone.utc
    )
