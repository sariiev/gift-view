from gift_view.db.models import Asset
from gift_view.db.repositories import AssetRepository


class AssetResolver:
    def __init__(self, repository: AssetRepository):
        self.repository = repository
        self.cache = {}


    def resolve(self, symbol: str) -> Asset:
        if symbol in self.cache:
            return self.cache[symbol]

        asset = self.repository.get_by_symbol(symbol=symbol)
        if asset:
            self.cache[symbol] = asset
            return asset

        asset = Asset(symbol=symbol)
        self.repository.add(asset=asset)

        self.repository.session.flush()

        self.cache[symbol] = asset
        return asset
