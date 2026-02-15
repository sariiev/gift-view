import pytest

from gift_view.db.repositories import MarketplaceRepository
from gift_view.db.resolvers import MarketplaceResolver


@pytest.mark.asyncio
async def test_resolve_creates_object(session):
    repository = MarketplaceRepository(session=session)
    resolver = MarketplaceResolver(repository=repository)

    name = "Fragment"
    marketplace = await resolver.resolve(name=name)
    assert marketplace.id is not None
    assert marketplace.name == name


@pytest.mark.asyncio
async def test_resolve_uses_cache(session):
    repository = MarketplaceRepository(session=session)
    resolver = MarketplaceResolver(repository=repository)

    name = "Fragment"
    marketplace1 = await resolver.resolve(name=name)
    marketplace2 = await resolver.resolve(name=name)

    assert marketplace1.id == marketplace2.id
