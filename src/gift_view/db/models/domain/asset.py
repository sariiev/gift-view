from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from gift_view.db.base import Base


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String(10), unique=True)
