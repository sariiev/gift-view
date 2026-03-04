from datetime import datetime
from typing import Optional, List, Tuple

from sqlalchemy import select, func, tuple_
from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.models import AssetPrice


class AssetPriceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_at_timestamps(self, keys: List[Tuple[int, datetime]]) -> List[AssetPrice]:
        if not keys:
            return []

        res = await self.session.execute(
            select(AssetPrice)
            .where(
                tuple_(AssetPrice.asset_id, AssetPrice.timestamp)
                .in_(keys)
            )
        )
        return list(res.scalars().all())


    async def get_latest_timestamp(self, asset_id: int) -> Optional[datetime]:
        res = await self.session.execute(
            select(func.max(AssetPrice.timestamp))
            .where(AssetPrice.asset_id == asset_id)
        )
        return res.scalar_one_or_none()


    async def get_latest_before(self, asset_id: int, timestamp: datetime) -> Optional[AssetPrice]:
        res = await self.session.execute(
            select(AssetPrice)
            .where(AssetPrice.asset_id == asset_id)
            .where(AssetPrice.timestamp <= timestamp)
            .order_by(AssetPrice.timestamp.desc())
            .limit(1)
        )
        return res.scalar_one_or_none()


    def add(self, asset_price: AssetPrice):
        self.session.add(asset_price)


    def add_all(self, asset_prices: List[AssetPrice]):
        self.session.add_all(asset_prices)
