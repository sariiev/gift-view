import pytest

from gift_view.db.repositories import AssetRepository
from gift_view.db.resolvers import AssetResolver


@pytest.mark.asyncio
async def test_resolve_creates_object(session):
    repository = AssetRepository(session=session)
    resolver = AssetResolver(repository=repository)

    symbol = "TON"
    asset = await resolver.resolve(symbol=symbol)
    assert asset.id is not None
    assert asset.symbol == symbol


@pytest.mark.asyncio
async def test_resolve_uses_cache(session):
    repository = AssetRepository(session=session)
    resolver = AssetResolver(repository=repository)

    symbol = "TON"
    asset1 = await resolver.resolve(symbol=symbol)
    asset2 = await resolver.resolve(symbol=symbol)

    assert asset1.id == asset2.id
