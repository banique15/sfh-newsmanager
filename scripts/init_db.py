"""Database initialization script."""

import sys
from pathlib import Path

from sqlalchemy import text

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import settings
from src.database.client import db_client
from src.database.models import Base


def create_tables() -> None:
    """Create all tables using SQLAlchemy models."""
    print("Creating tables using SQLAlchemy...")
    Base.metadata.create_all(bind=db_client.engine)
    print("✅ Tables created successfully!")


def run_migration(migration_file: Path) -> None:
    """Run a SQL migration file."""
    print(f"Running migration: {migration_file.name}...")
    
    with open(migration_file, "r", encoding="utf-8") as f:
        sql = f.read()
    
    session = db_client.get_session()
    try:
        # Split by semicolon and execute each statement
        statements = [s.strip() for s in sql.split(";") if s.strip()]
        for statement in statements:
            session.execute(text(statement))
        session.commit()
        print(f"✅ Migration {migration_file.name} completed!")
    except Exception as e:
        session.rollback()
        print(f"❌ Error running migration {migration_file.name}: {e}")
        raise
    finally:
        session.close()


def main() -> None:
    """Initialize database."""
    print("=" * 60)
    print("Newsletter Manager - Database Initialization")
    print("=" * 60)
    print()
    print(f"Database URL: {settings.database_url}")
    print()
    
    # Get migrations directory
    migrations_dir = Path(__file__).parent.parent / "migrations"
    
    if not migrations_dir.exists():
        print("❌ Migrations directory not found!")
        return
    
    # Get all .sql files sorted by name
    migration_files = sorted(migrations_dir.glob("*.sql"))
    
    if not migration_files:
        print("⚠️  No migration files found!")
        print("Creating tables using SQLAlchemy models only...")
        create_tables()
        return
    
    # Run migrations
    for migration_file in migration_files:
        run_migration(migration_file)
    
    print()
    print("=" * 60)
    print("✅ Database initialization complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
