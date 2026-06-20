from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from gift_view.db.base import Base


class Gift(Base):
    __tablename__ = "gifts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    models = relationship("Model", back_populates="gift")
    sales = relationship("Sale", back_populates="gift")
    backdrops = relationship(
        "Backdrop",
        secondary="gifts_backdrops",
        back_populates="gifts",
    )
    symbols = relationship(
        "Symbol",
        secondary="gifts_symbols",
        back_populates="gifts",
    )
