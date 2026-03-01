from typing import List

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_only

from gift_view.db.models import Sale


class SaleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def add_all(self, sales: List[Sale]):
        values = [
            {
                "marketplace_id": sale.marketplace_id,
                "marketplace_sale_id": sale.marketplace_sale_id,
                "gift_id": sale.gift_id,
                "gift_number": sale.gift_number,
                "model_id": sale.model_id,
                "backdrop_id": sale.backdrop_id,
                "symbol_id": sale.symbol_id,
                "asset_id": sale.asset_id,
                "price_native": sale.price_native,
                "price_usd": sale.price_usd,
                "timestamp": sale.timestamp
            } for sale in sales
        ]

        stmt = (
            insert(Sale)
            .values(values)
            .on_conflict_do_nothing(
                index_elements=["marketplace_id", "marketplace_sale_id"]
            )
        )

        await self.session.execute(stmt)
