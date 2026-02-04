"""Database models for articles."""

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


class Article(Base):
    """Article model matching the Supabase schema."""

    __tablename__ = "articles"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Core fields
    idx: Mapped[int] = mapped_column(Integer, default=0)
    news_title: Mapped[str] = mapped_column(String(200), nullable=False)
    news_excerpt: Mapped[str | None] = mapped_column(Text, nullable=True)
    newscontent: Mapped[str] = mapped_column(Text, nullable=False)
    news_content: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    # Image fields
    news_image: Mapped[str | None] = mapped_column(String, nullable=True)
    news_image_caption: Mapped[str | None] = mapped_column(String, nullable=True)

    # URL and author
    news_url: Mapped[str | None] = mapped_column(String, nullable=True)
    news_author: Mapped[str | None] = mapped_column(String, nullable=True)

    # Timestamps
    news_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    news_updated: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Status fields
    draft: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    news_status: Mapped[str | None] = mapped_column(String, nullable=True)
    featured: Mapped[bool] = mapped_column(Boolean, default=False)
    featured_order: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Additional fields
    news_categories: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    related_program: Mapped[str | None] = mapped_column(String, nullable=True)
    tiny: Mapped[str | None] = mapped_column(Text, nullable=True)
    sun: Mapped[Any | None] = mapped_column(JSON, nullable=True)

    def __repr__(self) -> str:
        """String representation."""
        status = "DRAFT" if self.draft else "PUBLISHED"
        return f"<Article(id={self.id}, title='{self.news_title}', status={status})>"

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "idx": self.idx,
            "news_title": self.news_title,
            "news_excerpt": self.news_excerpt,
            "newscontent": self.newscontent,
            "news_content": self.news_content,
            "news_image": self.news_image,
            "news_image_caption": self.news_image_caption,
            "news_url": self.news_url,
            "news_author": self.news_author,
            "news_date": self.news_date.isoformat() if self.news_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "news_updated": self.news_updated.isoformat() if self.news_updated else None,
            "draft": self.draft,
            "news_status": self.news_status,
            "featured": self.featured,
            "featured_order": self.featured_order,
            "news_categories": self.news_categories,
            "related_program": self.related_program,
            "tiny": self.tiny,
            "sun": self.sun,
        }
