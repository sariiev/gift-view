from gift_view.db.models import Backdrop
from gift_view.db.repositories import BackdropRepository


class BackdropResolver:
    def __init__(self, repository: BackdropRepository):
        self.repository = repository
        self.cache = {}


    def resolve(self, name: str, rarity_percent: float) -> Backdrop:
        key = (name, rarity_percent)
        if key in self.cache:
            return self.cache[key]

        backdrop = self.repository.get_by_name_and_rarity_percent(name=name, rarity_percent=rarity_percent)
        if backdrop:
            self.cache[key] = backdrop
            return backdrop

        backdrop = Backdrop(name=name, rarity_percent=rarity_percent)
        self.repository.add(backdrop=backdrop)

        self.repository.session.flush()

        self.cache[key] = backdrop
        return backdrop
