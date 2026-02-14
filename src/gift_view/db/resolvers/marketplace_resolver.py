from gift_view.db.models import Marketplace
from gift_view.db.repositories import MarketplaceRepository


class MarketplaceResolver:
    def __init__(self, repository: MarketplaceRepository):
        self.repository = repository
        self.cache = {}


    def resolve(self, name: str) -> Marketplace:
        if name in self.cache:
            return self.cache[name]

        marketplace = self.repository.get_by_name(name=name)
        if marketplace:
            self.cache[name] = marketplace
            return marketplace

        marketplace = Marketplace(name=name)
        self.repository.add(marketplace=marketplace)

        self.repository.session.flush()

        self.cache[name] = marketplace
        return marketplace
