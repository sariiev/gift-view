from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.models import Sale


class SaleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    def add(self, sale: Sale):
        self.session.add(sale)


    def add_all(self, sales: List[Sale]):
        self.session.add_all(sales)
