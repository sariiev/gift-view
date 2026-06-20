import pytest
import pytest_asyncio

from gift_view.db.resolvers import ModelResolver, GiftResolver


@pytest_asyncio.fixture
async def gift_id(session):
    resolver = GiftResolver()

    name = "Plush Pepe"
    return await resolver.resolve_id(session=session, name=name)


@pytest.mark.asyncio
async def test_resolve_creates_object(session, gift_id):
    resolver = ModelResolver()

    name = "Gold"
    is_crafted = False
    rarity_percent = 0.05
    model_id = await resolver.resolve_id(session=session, gift_id=gift_id, name=name, is_crafted=is_crafted, rarity_percent=rarity_percent)
    assert model_id is not None

@pytest.mark.asyncio
async def test_resolve_uses_cache(session, gift_id):
    resolver = ModelResolver()

    name = "Gold"
    is_crafted = False
    rarity_percent = 0.05
    model1_id = await resolver.resolve_id(session=session, gift_id=gift_id, name=name, is_crafted=is_crafted, rarity_percent=rarity_percent)
    model2_id = await resolver.resolve_id(session=session, gift_id=gift_id, name=name, is_crafted=is_crafted, rarity_percent=rarity_percent)

    assert model1_id == model2_id
