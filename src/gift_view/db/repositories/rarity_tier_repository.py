from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from gift_view.db.models import RarityTier


class RarityTierRepository:
    def __init__(self, session: Session):
        self.session = session


    def get_by_name(self, name: str) -> Optional[RarityTier]:
        return self.session.execute(
            select(RarityTier)
            .where(RarityTier.name == name)
        ).scalar_one_or_none()


    def add(self, rarity_tier: RarityTier):
        self.session.add(rarity_tier)
