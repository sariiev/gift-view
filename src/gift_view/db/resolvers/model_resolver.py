

from gift_view.db.models import Model, Gift
from gift_view.db.repositories import ModelRepository


class ModelResolver:
    def __init__(self, repository: ModelRepository):
        self.repository = repository
        self.cache = {}


    async def resolve(self, gift: Gift, name: str, is_crafted: bool, rarity_percent: float) -> Model:
        key = (gift.id, name, is_crafted)
        if key in self.cache:
            return self.cache[key]

        model = await self.repository.get_by_gift_and_name_and_crafted(gift=gift, name=name, is_crafted=is_crafted)
        if model:
            self.cache[key] = model
            return model

        model = Model(gift_id=gift.id, name=name, is_crafted=is_crafted, rarity_percent=rarity_percent)

        self.repository.add(model=model)

        await self.repository.session.flush()

        self.cache[key] = model
        return model
