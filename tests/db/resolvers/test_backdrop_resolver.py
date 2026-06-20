import pytest

from gift_view.db.resolvers import BackdropResolver


@pytest.mark.asyncio
async def test_resolve_creates_object(session):
    resolver = BackdropResolver()

    name = "Black"
    rarity_percent = 0.05
    backdrop_id = await resolver.resolve_id(session=session, name=name, rarity_percent=rarity_percent)
    assert backdrop_id is not None


@pytest.mark.asyncio
async def test_resolve_uses_cache(session):
    resolver = BackdropResolver()

    name = "Black"
    rarity_percent = 0.05
    backdrop1_id = await resolver.resolve_id(session=session, name=name, rarity_percent=rarity_percent)
    backdrop2_id = await resolver.resolve_id(session=session, name=name, rarity_percent=rarity_percent)

    assert backdrop1_id == backdrop2_id
