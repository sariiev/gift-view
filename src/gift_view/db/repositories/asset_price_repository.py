from datetime import datetime
from typing import Optional, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.models import Asset, AssetPrice


class AssetPriceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_latest_timestamp(self, asset: Asset) -> Optional[datetime]:
        res = await self.session.execute(
            select(func.max(AssetPrice.timestamp))
            .where(AssetPrice.asset_id == asset.id)
        )
        return res.scalar_one_or_none()


    async def get_latest_before(self, asset: Asset, timestamp: datetime) -> Optional[AssetPrice]:
        res = await self.session.execute(
            select(AssetPrice)
            .where(AssetPrice.asset_id == asset.id)
            .where(AssetPrice.timestamp <= timestamp)
            .order_by(AssetPrice.timestamp.desc())
            .limit(1)
        )
        return res.scalar_one_or_none()


    def add(self, asset_price: AssetPrice):
        self.session.add(asset_price)


    def add_all(self, asset_prices: List[AssetPrice]):
        self.session.add_all(asset_prices)
