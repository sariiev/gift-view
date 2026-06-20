import pytest

from gift_view.db.resolvers import AssetResolver


@pytest.mark.asyncio
async def test_resolve_creates_object(session):
    resolver = AssetResolver()

    symbol = "TON"
    asset_id = await resolver.resolve_id(session=session, symbol=symbol)
    assert asset_id is not None


@pytest.mark.asyncio
async def test_resolve_uses_cache(session):
    resolver = AssetResolver()

    symbol = "TON"
    asset1_id = await resolver.resolve_id(session=session, symbol=symbol)
    asset2_id = await resolver.resolve_id(session=session, symbol=symbol)

    assert asset1_id == asset2_id
