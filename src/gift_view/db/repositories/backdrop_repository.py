from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from gift_view.db.models import Backdrop


class BackdropRepository:
    def __init__(self, session: Session):
        self.session = session


    def get_by_name_and_rarity_percent(self, name: str, rarity_percent: float) -> Optional[Backdrop]:
        return self.session.execute(
            select(Backdrop)
            .where(Backdrop.name == name)
            .where(Backdrop.rarity_percent == rarity_percent)
        ).scalar_one_or_none()


    def add(self, backdrop: Backdrop):
        self.session.add(backdrop)
