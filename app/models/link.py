from datetime import datetime

from sqlalchemy import Text, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base


class Link(Base):
    __tablename__ = "links"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(Text, index=True, unique=True)
    original_url: Mapped[str] = mapped_column(Text)
    clicks: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"Link(id={self.id!r})"
