from gift_view.db.repositories import GiftRepository
from gift_view.db.resolvers import GiftResolver


def test_resolve_creates_object(session):
    repository = GiftRepository(session=session)
    resolver = GiftResolver(repository=repository)

    name = "Plush Pepe"
    gift = resolver.resolve(name=name)
    assert gift.id is not None
    assert gift.name == name


def test_resolve_uses_cache(session):
    repository = GiftRepository(session=session)
    resolver = GiftResolver(repository=repository)

    name = "Plush Pepe"
    gift1 = resolver.resolve(name=name)
    gift2 = resolver.resolve(name=name)

    assert gift1.id == gift2.id
