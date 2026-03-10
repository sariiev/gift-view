import re
from datetime import datetime, timezone
from typing import Dict, List

from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.models.domain import Sale
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



    async def parse_sales(self, session: AsyncSession, sales: Dict | List):
        result = []

        marketplace_id = await self.marketplace_resolver.resolve_id(
            session=session,
            name=self.marketplace_name
        )

        for item in sales:
            gift_id = await self.gift_resolver.resolve_id(
                session=session,
                name=item["gift_name"],
                create=True
            )

            model_name, model_rarity, model_is_crafted = self.parse_model_string(raw=item["model"])
            model_id = await self.model_resolver.resolve_id(
                session=session,
                gift_id=gift_id,
                name=model_name,
                is_crafted=model_is_crafted,
                rarity_percent=model_rarity
            )

            backdrop_name, backdrop_rarity = self.parse_attribute_string(raw=item["backdrop"])
            backdrop_id = await self.backdrop_resolver.resolve_id(
                session=session,
                name=backdrop_name,
                rarity_percent=backdrop_rarity
            )

            symbol_name, symbol_rarity = self.parse_attribute_string(raw=item["symbol"])
            symbol_id = await self.symbol_resolver.resolve_id(
                session=session,
                name=symbol_name,
                rarity_percent=symbol_rarity
            )

            asset_id = await self.asset_resolver.resolve_id(
                session=session,
                symbol=item["asset"]
            )

            sale = Sale(
                marketplace_id=marketplace_id,
                marketplace_sale_id=item["_id"],
                gift_id=gift_id,
                gift_number=int(item["gift_num"]),
                model_id=model_id,
                backdrop_id=backdrop_id,
                symbol_id=symbol_id,
                asset_id=asset_id,
                price_native=float(item["price"]),
                timestamp=datetime.strptime(item["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
            )

            result.append(sale)
        return result


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
