from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.models.domain import Model
from gift_view.db.repositories.domain import ModelRepository


class ModelResolver:
    def __init__(self):
        self.cache = {}


    async def resolve_id(self, session: AsyncSession, gift_id: int, name: str, create: bool, is_crafted: Optional[bool] = None, rarity_percent: Optional[float] = None) -> Optional[int]:
        key = (gift_id, name, is_crafted)
        if key in self.cache:
            return self.cache[key]

        repository = ModelRepository(session=session)
        model = await repository.get_by_gift_id_and_name(gift_id=gift_id, name=name)

        if model:
            self.cache[key] = model.id
            return model.id

        if not create:
            return None

        model = Model(gift_id=gift_id, name=name, is_crafted=is_crafted, rarity_percent=rarity_percent)

        repository.add(model)

        await session.flush()

        self.cache[key] = model.id
        return model.id
