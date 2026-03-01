from typing import List

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.models import Asset


class AssetRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_all(self) -> List[Asset]:
        res = await self.session.execute(
            select(Asset)
        )

        return list(res.scalars().all())


    async def get_or_create(self, symbol: str) -> Asset:
        stmt = insert(Asset).values(symbol=symbol).on_conflict_do_nothing(index_elements=["symbol"])

        await self.session.execute(stmt)

        res = await self.session.execute(
            select(Asset).where(Asset.symbol == symbol)
        )
        return res.scalar_one()
