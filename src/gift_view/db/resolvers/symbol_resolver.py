from gift_view.db.models import Symbol
from gift_view.db.repositories import SymbolRepository


class SymbolResolver:
    def __init__(self, repository: SymbolRepository):
        self.repository = repository
        self.cache = {}


    def resolve(self, name: str, rarity_percent: float) -> Symbol:
        key = (name, rarity_percent)
        if key in self.cache:
            return self.cache[key]

        symbol = self.repository.get_by_name_and_rarity_percent(name=name, rarity_percent=rarity_percent)
        if symbol:
            self.cache[key] = symbol
            return symbol

        symbol = Symbol(name=name, rarity_percent=rarity_percent)
        self.repository.add(symbol=symbol)

        self.repository.session.flush()

        self.cache[key] = symbol
        return symbol
