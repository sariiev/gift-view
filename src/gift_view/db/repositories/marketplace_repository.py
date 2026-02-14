from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from gift_view.db.models import Marketplace


class MarketplaceRepository:
    def __init__(self, session: Session):
        self.session = session


    def get_by_name(self, name: str) -> Optional[Marketplace]:
        return self.session.execute(
            select(Marketplace)
            .where(Marketplace.name == name)
        ).scalar_one_or_none()


    def add(self, marketplace: Marketplace):
        self.session.add(marketplace)
