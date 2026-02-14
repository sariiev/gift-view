from sqlalchemy.orm import Session

from gift_view.db.models import Sale


class SaleRepository:
    def __init__(self, session: Session):
        self.session = session


    def add(self, sale: Sale):
        self.session.add(sale)
