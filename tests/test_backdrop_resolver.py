from gift_view.db.repositories import BackdropRepository
from gift_view.db.resolvers import BackdropResolver


def test_resolve_creates_object(session):
    repository = BackdropRepository(session=session)
    resolver = BackdropResolver(repository=repository)

    name = "Black"
    rarity_percent = 0.05
    backdrop = resolver.resolve(name=name, rarity_percent=rarity_percent)
    assert backdrop.id is not None
    assert backdrop.name == name
    assert backdrop.rarity_percent == rarity_percent


def test_resolve_uses_cache(session):
    repository = BackdropRepository(session=session)
    resolver = BackdropResolver(repository=repository)

    name = "Black"
    rarity_percent = 0.05
    backdrop1 = resolver.resolve(name=name, rarity_percent=rarity_percent)
    backdrop2 = resolver.resolve(name=name, rarity_percent=rarity_percent)

    assert backdrop1.id == backdrop2.id
