from gift_view.db.models import Gift
from gift_view.db.repositories import GiftRepository


class GiftResolver:
    def __init__(self, repository: GiftRepository):
        self.repository = repository
        self.cache = {}


    def resolve(self, name: str) -> Gift:
        if name in self.cache:
            return self.cache[name]

        gift = self.repository.get_by_name(name=name)
        if gift:
            self.cache[name] = gift
            return gift

        gift = Gift(name=name)
        self.repository.add(gift=gift)

        self.repository.session.flush()

        self.cache[name] = gift
        return gift
