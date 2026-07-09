from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class Poem(Base):
    __tablename__ = "poems"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    topic: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    critic_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    iteration: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    telegram_message_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    generated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )