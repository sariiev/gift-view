import pytest

from gift_view.db.resolvers import SymbolResolver


@pytest.mark.asyncio
async def test_resolve_creates_object(session):
    resolver = SymbolResolver()

    name = "Star"
    rarity_percent = 0.05
    symbol_id = await resolver.resolve_id(session=session, name=name, rarity_percent=rarity_percent)
    assert symbol_id is not None


@pytest.mark.asyncio
async def test_resolve_uses_cache(session):
    resolver = SymbolResolver()

    name = "Star"
    rarity_percent = 0.05
    symbol1_id = await resolver.resolve_id(session=session, name=name, rarity_percent=rarity_percent)
    symbol2_id = await resolver.resolve_id(session=session, name=name, rarity_percent=rarity_percent)

    assert symbol1_id == symbol2_id
