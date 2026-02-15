import pytest
import pytest_asyncio

from gift_view.db.repositories import ModelRepository, GiftRepository
from gift_view.db.resolvers import ModelResolver, GiftResolver


@pytest_asyncio.fixture
async def gift(session):
    repository = GiftRepository(session=session)
    resolver = GiftResolver(repository=repository)

    name = "Plush Pepe"
    return await resolver.resolve(name)


@pytest.mark.asyncio
async def test_resolve_creates_object(session, gift):
    repository = ModelRepository(session=session)
    resolver = ModelResolver(repository=repository)

    name = "Gold"
    is_crafted = False
    rarity_percent = 0.05
    rarity_tier = None
    model = await resolver.resolve(gift=gift, name=name, is_crafted=is_crafted, rarity_percent=rarity_percent, rarity_tier=rarity_tier)
    assert model.id is not None
    assert model.name == name
    assert model.is_crafted == is_crafted
    assert model.rarity_percent == rarity_percent
    assert model.rarity_tier == rarity_tier


@pytest.mark.asyncio
async def test_resolve_uses_cache(session, gift):
    repository = ModelRepository(session=session)
    resolver = ModelResolver(repository=repository)

    name = "Gold"
    is_crafted = False
    rarity_percent = 0.05
    rarity_tier = None
    model1 = await resolver.resolve(gift=gift, name=name, is_crafted=is_crafted, rarity_percent=rarity_percent, rarity_tier=rarity_tier)
    model2 = await resolver.resolve(gift=gift, name=name, is_crafted=is_crafted, rarity_percent=rarity_percent, rarity_tier=rarity_tier)

    assert model1.id == model2.id
