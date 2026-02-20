from abc import ABC, abstractmethod
from typing import Dict, List

from gift_view.db.resolvers import MarketplaceResolver, GiftResolver, ModelResolver, BackdropResolver, SymbolResolver, \
    AssetResolver


class BaseMarketplaceParser(ABC):
    def __init__(
            self,
            marketplace_resolver: MarketplaceResolver,
            gift_resolver: GiftResolver,
            model_resolver: ModelResolver,
            backdrop_resolver: BackdropResolver,
            symbol_resolver: SymbolResolver,
            asset_resolver: AssetResolver
    ):
        self.marketplace_resolver = marketplace_resolver
        self.gift_resolver = gift_resolver
        self.model_resolver = model_resolver
        self.backdrop_resolver = backdrop_resolver
        self.symbol_resolver = symbol_resolver
        self.asset_resolver = asset_resolver


    @abstractmethod
    async def parse_sales(self, sales: Dict | List):
        pass