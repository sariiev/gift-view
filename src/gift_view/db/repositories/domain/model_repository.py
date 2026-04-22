from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.models.domain import Model


class ModelRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_by_gift_id_and_params(
            self,
            gift_id: int,
            name: str,
            is_crafted: bool,
            rarity_percent: float
    ) -> Optional[Model]:
        res = await self.session.execute(
            select(Model)
            .where(Model.gift_id == gift_id)
            .where(Model.name == name)
            .where(Model.is_crafted == is_crafted)
            .where(Model.rarity_percent == rarity_percent)
        )

        return res.scalar_one_or_none()


    def add(self, model: Model):
        self.session.add(model)
