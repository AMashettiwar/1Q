from datetime import date, datetime
from sqlalchemy import (Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text,
                        UniqueConstraint)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(120), default="")
    avatar: Mapped[str] = mapped_column(String(16), default="🧬")
    role: Mapped[str | None] = mapped_column(String(60), nullable=True)
    base_rating: Mapped[float] = mapped_column(Float, default=1000.0)
    placement_done: Mapped[bool] = mapped_column(Boolean, default=False)
    points: Mapped[int] = mapped_column(Integer, default=0)
    streak: Mapped[int] = mapped_column(Integer, default=0)
    best_streak: Mapped[int] = mapped_column(Integer, default=0)
    last_completed: Mapped[date | None] = mapped_column(Date, nullable=True)
    shields: Mapped[int] = mapped_column(Integer, default=0)
    unlocked_json: Mapped[str] = mapped_column(Text, default="[]")
    equipped: Mapped[str] = mapped_column(String(40), default="")
    title: Mapped[str] = mapped_column(String(60), default="Curious Cell")
    reminder_opt_in: Mapped[bool] = mapped_column(Boolean, default=True)
    last_reminded: Mapped[date | None] = mapped_column(Date, nullable=True)
    theme: Mapped[str] = mapped_column(String(20), default="ivory")
    timezone: Mapped[str] = mapped_column(String(64), default="")
    soft_flags: Mapped[int] = mapped_column(Integer, default=0)
    honest_days: Mapped[int] = mapped_column(Integer, default=0)
    last_seen: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now())


class Mastery(Base):
    __tablename__ = "mastery"
    __table_args__ = (UniqueConstraint("user_id", "subtopic"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    subtopic: Mapped[str] = mapped_column(String(80))
    rating: Mapped[float] = mapped_column(Float, default=1000.0)
    seen: Mapped[int] = mapped_column(Integer, default=0)


class DailySet(Base):
    __tablename__ = "daily_sets"
    __table_args__ = (UniqueConstraint("user_id", "day"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    day: Mapped[date] = mapped_column(Date)
    questions_json: Mapped[str] = mapped_column(Text)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)


class Answer(Base):
    __tablename__ = "answers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    day: Mapped[date] = mapped_column(Date, index=True)
    question_id: Mapped[str] = mapped_column(String(80))
    concept_id: Mapped[str] = mapped_column(String(120))
    subtopic: Mapped[str] = mapped_column(String(80))
    correct: Mapped[bool] = mapped_column(Boolean)
    is_placement: Mapped[bool] = mapped_column(Boolean, default=False)
    elapsed_ms: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now())


class ReviewItem(Base):
    """A missed concept waiting to come back as a reworded question."""
    __tablename__ = "review_items"
    __table_args__ = (UniqueConstraint("user_id", "concept_id"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    concept_id: Mapped[str] = mapped_column(String(120))
    subtopic: Mapped[str] = mapped_column(String(80))
    question_json: Mapped[str] = mapped_column(Text)
    due: Mapped[date] = mapped_column(Date)
    stage: Mapped[int] = mapped_column(Integer, default=0)
    retired: Mapped[bool] = mapped_column(Boolean, default=False)


class RankSnapshot(Base):
    __tablename__ = "rank_snapshots"
    __table_args__ = (UniqueConstraint("user_id", "day"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    day: Mapped[date] = mapped_column(Date)
    rank: Mapped[int] = mapped_column(Integer)


class PointEvent(Base):
    """Points earned per user per day. Powers daily/weekly/monthly boards."""
    __tablename__ = "point_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    day: Mapped[date] = mapped_column(Date, index=True)
    points: Mapped[int] = mapped_column(Integer)
