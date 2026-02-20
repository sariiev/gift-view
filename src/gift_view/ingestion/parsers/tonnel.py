import re
from datetime import datetime, timezone
from typing import Dict, List

from gift_view.db.models import Sale
from gift_view.db.resolvers import MarketplaceResolver, GiftResolver, ModelResolver, BackdropResolver, SymbolResolver, \
    AssetResolver
from gift_view.ingestion.parsers import BaseMarketplaceParser


class TonnelParser(BaseMarketplaceParser):
    def __init__(
            self,
            marketplace_resolver: MarketplaceResolver,
            gift_resolver: GiftResolver,
            model_resolver: ModelResolver,
            backdrop_resolver: BackdropResolver,
            symbol_resolver: SymbolResolver,
            asset_resolver: AssetResolver
    ):
        super().__init__(
            marketplace_resolver=marketplace_resolver,
            gift_resolver=gift_resolver,
            model_resolver=model_resolver,
            backdrop_resolver=backdrop_resolver,
            symbol_resolver=symbol_resolver,
            asset_resolver=asset_resolver
        )
        self.marketplace_name = "Tonnel"
        self.ATTRIBUTE_PATTERN = re.compile(r"^(?P<name>.+?)\s*\((?P<rarity>[\d.]+)%\)$")



    async def parse_sales(self, sales: Dict | List):
        result = []

        marketplace = await self.marketplace_resolver.resolve(name=self.marketplace_name)

        for item in sales:
            gift = await self.gift_resolver.resolve(name=item["gift_name"])

            model_name, model_rarity, model_is_crafted = self.parse_model_string(raw=item["model"])
            model = await self.model_resolver.resolve(
                gift=gift,
                name=model_name,
                is_crafted=model_is_crafted,
                rarity_percent=model_rarity
            )

            backdrop_name, backdrop_rarity = self.parse_attribute_string(raw=item["backdrop"])
            backdrop = await self.backdrop_resolver.resolve(
                name=backdrop_name,
                rarity_percent=backdrop_rarity
            )

            symbol_name, symbol_rarity = self.parse_attribute_string(raw=item["symbol"])
            symbol = await self.symbol_resolver.resolve(
                name=symbol_name,
                rarity_percent=symbol_rarity
            )

            asset = await self.asset_resolver.resolve(symbol=item["asset"])

            sale = Sale(
                marketplace_id=marketplace.id,
                gift_id=gift.id,
                gift_number=item["gift_num"],
                model_id=model.id,
                backdrop_id=backdrop.id,
                symbol_id=symbol.id,
                asset_id=asset.id,
                price_native=float(item["price"]),
                timestamp=datetime.strptime(item["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
            )

            result.append(sale)
        return sales


    def parse_attribute_string(self, raw: str):
        match = self.ATTRIBUTE_PATTERN.match(raw.strip())
        if not match:
            raise ValueError(f"Invalid attribute format: {raw}")

        name = match.group("name").strip()
        rarity = float(match.group("rarity"))

        return name, rarity


    def parse_model_string(self, raw: str):
        name, rarity = self.parse_attribute_string(raw=raw)
        if rarity == 0:
            return name, rarity, True
        else:
            return name, rarity, False
