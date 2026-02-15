import pytest

from gift_view.db.repositories import RarityTierRepository
from gift_view.db.resolvers import RarityTierResolver


@pytest.mark.asyncio
async def test_resolve_creates_object(session):
    repository = RarityTierRepository(session=session)
    resolver = RarityTierResolver(repository=repository)

    name = "Legendary"
    rarity_tier = await resolver.resolve(name=name)
    assert rarity_tier.id is not None
    assert rarity_tier.name == name


@pytest.mark.asyncio
async def test_resolve_uses_cache(session):
    repository = RarityTierRepository(session=session)
    resolver = RarityTierResolver(repository=repository)

    name = "Legendary"
    rarity_tier1 = await resolver.resolve(name=name)
    rarity_tier2 = await resolver.resolve(name=name)

    assert rarity_tier1.id == rarity_tier2.id
