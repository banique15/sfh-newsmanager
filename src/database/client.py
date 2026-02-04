"""Database client for Supabase connection."""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from supabase import Client, create_client

from src.config.settings import settings


class DatabaseClient:
    """Database client manager."""

    def __init__(self) -> None:
        """Initialize database clients."""
        # SQLAlchemy engine
        self.engine = create_engine(
            settings.database_url,
            pool_size=settings.db_pool_max,
            max_overflow=0,
            echo=settings.debug,
        )
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )

        # Supabase client (for storage and realtime features)
        self.supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_key,
        )

    def get_session(self) -> Session:
        """Get a database session."""
        return self.SessionLocal()

    def close(self) -> None:
        """Close database connections."""
        self.engine.dispose()


# Global database client
db_client = DatabaseClient()


def get_db() -> Session:
    """Dependency for getting database session."""
    session = db_client.get_session()
    try:
        yield session
    finally:
        session.close()
