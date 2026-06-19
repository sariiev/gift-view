import pytest

from gift_view.db.resolvers import GiftResolver


@pytest.mark.asyncio
async def test_resolve_creates_object(session):
    resolver = GiftResolver()

    name = "Plush Pepe"
    gift_id = await resolver.resolve_id(session=session, name=name, create=True)
    print(f"GIFT ID: {gift_id}")
    assert gift_id is not None


@pytest.mark.asyncio
async def test_resolve_uses_cache(session):
    resolver = GiftResolver()

    name = "Plush Pepe"
    gift1_id = await resolver.resolve_id(session=session, name=name, create=True)
    gift2_id = await resolver.resolve_id(session=session, name=name, create=True)

    assert gift1_id == gift2_id
