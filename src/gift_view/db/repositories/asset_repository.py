from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.models import Asset


class AssetRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_by_symbol(self, symbol: str) -> Optional[Asset]:
        res = await self.session.execute(
            select(Asset)
            .where(Asset.symbol == symbol)
        )
        return res.scalar_one_or_none()


    def add(self, asset: Asset):
        self.session.add(asset)
