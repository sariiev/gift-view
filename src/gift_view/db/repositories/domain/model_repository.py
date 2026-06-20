from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.models.domain import Model


class ModelRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_by_gift_id_and_name(
            self,
            gift_id: int,
            name: str,
    ) -> Optional[Model]:
        res = await self.session.execute(
            select(Model)
            .where(Model.gift_id == gift_id)
            .where(Model.name == name)
        )

        return res.scalar_one_or_none()

    async def get_by_gift_id(
            self,
            gift_id: int
    ):
        res = await self.session.execute(
            select(Model)
            .where(Model.gift_id == gift_id)
        )

        return list(res.scalars().all())


    def add(self, model: Model):
        self.session.add(model)
