from datetime import datetime
from importlib.resources import files
from typing import Optional, List

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.models.aggregation import GiftModelPriceBar

SQL = text(
    files("gift_view.sql.aggregation")
    .joinpath("gift_model_price_bar.sql")
    .read_text()
)

class GiftModelPriceBarRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_latest_timestamp(self, interval: str) -> Optional[datetime]:
        res = await self.session.execute(
            select(GiftModelPriceBar.timestamp)
            .where(GiftModelPriceBar.interval == interval)
            .order_by(GiftModelPriceBar.timestamp.desc())
            .limit(1)
        )

        return res.scalar_one_or_none()


    async def get_bars(
            self,
            gift_id: int,
            model_id: int,
            interval: str,
            limit: int,
            before: datetime | None = None
    ) -> List[GiftModelPriceBar]:
        query = (
            select(GiftModelPriceBar)
            .where(GiftModelPriceBar.gift_id == gift_id)
            .where(GiftModelPriceBar.model_id == model_id)
            .where(GiftModelPriceBar.interval == interval)
        )

        if before:
            query = query.where(GiftModelPriceBar.timestamp < before)

        query = (
            query
            .order_by(GiftModelPriceBar.timestamp.desc())
            .limit(limit)
        )

        res = await self.session.execute(query)

        return list(res.scalars().all())


    async def aggregate(self, interval: str, start: datetime):
        await self.session.execute(
            SQL,
            {
                "start": start,
                "interval": interval
            }
        )
