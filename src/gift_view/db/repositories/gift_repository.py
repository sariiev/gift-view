from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from gift_view.db.models import Gift


class GiftRepository:
    def __init__(self, session: Session):
        self.session = session


    def get_by_name(self, name: str) -> Optional[Gift]:
        return self.session.execute(
            select(Gift)
            .where(Gift.name == name)
        ).scalar_one_or_none()


    def add(self, gift: Gift):
        self.session.add(gift)
