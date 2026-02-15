import pytest

from gift_view.db.repositories import GiftRepository
from gift_view.db.resolvers import GiftResolver


@pytest.mark.asyncio
async def test_resolve_creates_object(session):
    repository = GiftRepository(session=session)
    resolver = GiftResolver(repository=repository)

    name = "Plush Pepe"
    gift = await resolver.resolve(name=name)
    assert gift.id is not None
    assert gift.name == name


@pytest.mark.asyncio
async def test_resolve_uses_cache(session):
    repository = GiftRepository(session=session)
    resolver = GiftResolver(repository=repository)

    name = "Plush Pepe"
    gift1 = await resolver.resolve(name=name)
    gift2 = await resolver.resolve(name=name)

    assert gift1.id == gift2.id
