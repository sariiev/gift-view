from gift_view.db.repositories import SymbolRepository
from gift_view.db.resolvers import SymbolResolver


def test_resolve_creates_object(session):
    repository = SymbolRepository(session=session)
    resolver = SymbolResolver(repository=repository)

    name = "Star"
    rarity_percent = 0.05
    symbol = resolver.resolve(name=name, rarity_percent=rarity_percent)
    assert symbol.id is not None
    assert symbol.name == name
    assert symbol.rarity_percent == rarity_percent


def test_resolve_uses_cache(session):
    repository = SymbolRepository(session=session)
    resolver = SymbolResolver(repository=repository)

    name = "Star"
    rarity_percent = 0.05
    symbol1 = resolver.resolve(name=name, rarity_percent=rarity_percent)
    symbol2 = resolver.resolve(name=name, rarity_percent=rarity_percent)

    assert symbol1.id == symbol2.id
