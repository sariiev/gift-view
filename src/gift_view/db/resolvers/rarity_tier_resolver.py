from gift_view.db.models import RarityTier
from gift_view.db.repositories import RarityTierRepository


class RarityTierResolver:
    def __init__(self, repository: RarityTierRepository):
        self.repository = repository
        self.cache = {}


    async def resolve(self, name: str) -> RarityTier:
        if name in self.cache:
            return self.cache[name]

        rarity_tier = await self.repository.get_by_name(name=name)
        if rarity_tier:
            self.cache[name] = rarity_tier
            return rarity_tier

        rarity_tier = RarityTier(name=name)
        self.repository.add(rarity_tier=rarity_tier)

        await self.repository.session.flush()

        self.cache[name] = rarity_tier
        return rarity_tier
