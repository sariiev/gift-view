from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from gift_view.db.base import Base


class Marketplace(Base):
    __tablename__ = "marketplaces"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)
    sales = relationship("Sale", back_populates="marketplace")
