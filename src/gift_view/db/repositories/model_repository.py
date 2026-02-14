from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from gift_view.db.models import Model, Gift


class ModelRepository:
    def __init__(self, session: Session):
        self.session = session


    def get_by_gift_and_name_and_crafted(self, gift: Gift, name: str, is_crafted: bool) -> Optional[Model]:
        return self.session.execute(
            select(Model)
            .where(Model.gift_id == gift.id)
            .where(Model.name == name)
            .where(Model.is_crafted == is_crafted)
        ).scalar_one_or_none()


    def add(self, model: Model):
        self.session.add(model)
