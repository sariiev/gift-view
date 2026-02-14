from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from gift_view.db.models import Asset


class AssetRepository:
    def __init__(self, session: Session):
        self.session = session


    def get_by_symbol(self, symbol: str) -> Optional[Asset]:
        return self.session.execute(
            select(Asset)
            .where(Asset.symbol == symbol)
        ).scalar_one_or_none()


    def add(self, asset: Asset):
        self.session.add(asset)
