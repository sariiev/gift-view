from datetime import datetime, timezone
from typing import Dict, Any

from sqlalchemy import ForeignKey, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from gift_view.db.base import Base


class MarketplaceState(Base):
    __tablename__ = "marketplaces_states"

    marketplace_id: Mapped[int] = mapped_column(
        ForeignKey("marketplaces.id"),
        primary_key=True
    )
    state: Mapped[Dict[str, Any]] = mapped_column(JSON)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )