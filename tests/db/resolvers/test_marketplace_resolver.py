import pytest

from gift_view.db.resolvers import MarketplaceResolver


@pytest.mark.asyncio
async def test_resolve_creates_object(session):
    resolver = MarketplaceResolver()

    name = "Fragment"
    marketplace_id = await resolver.resolve_id(session=session, name=name)
    assert marketplace_id is not None


@pytest.mark.asyncio
async def test_resolve_uses_cache(session):
    resolver = MarketplaceResolver()

    name = "Fragment"
    marketplace1_id = await resolver.resolve_id(session=session, name=name)
    marketplace2_id = await resolver.resolve_id(session=session, name=name)

    assert marketplace1_id == marketplace2_id
