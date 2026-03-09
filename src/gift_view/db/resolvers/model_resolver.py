from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.repositories.domain import ModelRepository


class ModelResolver:
    def __init__(self):
        self.cache = {}


    async def resolve_id(self, session: AsyncSession, gift_id: int, name: str, is_crafted: bool, rarity_percent: float) -> int:
        key = (gift_id, name, is_crafted)
        if key in self.cache:
            return self.cache[key]

        repository = ModelRepository(session=session)
        model = await repository.get_or_create(gift_id=gift_id, name=name, is_crafted=is_crafted, rarity_percent=rarity_percent)

        self.cache[key] = model.id
        return model.id
