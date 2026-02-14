

from gift_view.db.models import Model, Gift
from gift_view.db.models.rarity_tier import RarityTier
from gift_view.db.repositories import ModelRepository


class ModelResolver:
    def __init__(self, repository: ModelRepository):
        self.repository = repository
        self.cache = {}


    def resolve(self, gift: Gift, name: str, is_crafted: bool, rarity_percent: float | None = None, rarity_tier: RarityTier | None = None) -> Model:
        key = (gift.id, name, is_crafted)
        if key in self.cache:
            return self.cache[key]

        model = self.repository.get_by_gift_and_name_and_crafted(gift=gift, name=name, is_crafted=is_crafted)
        if model:
            self.cache[key] = model
            return model

        if is_crafted:
            model = Model(gift_id=gift.id, name=name, is_crafted=is_crafted, rarity_percent=None, rarity_tier_id=rarity_tier.id)
        else:
            model = Model(gift_id=gift.id, name=name, is_crafted=is_crafted, rarity_percent=rarity_percent, rarity_tier_id=None)
        self.repository.add(model=model)

        self.repository.session.flush()

        self.cache[key] = model
        return model
