"""Test database connection."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import settings
from src.database import News, get_db


def main() -> None:
    """Test database connection and query news articles."""
    print("=" * 60)
    print("Newsletter Manager - Database Connection Test")
    print("=" * 60)
    print()
    print(f"Database URL: {settings.database_url[:50]}...")
    print()
    
    # Get database session
    session = next(get_db())
    
    try:
        # Test query: count articles
        total_count = session.query(News).count()
        print(f"✅ Connection successful!")
        print(f"Total articles: {total_count}")
        print()
        
        # Get draft vs published counts
        draft_count = session.query(News).filter(News.draft == True).count()
        published_count = session.query(News).filter(News.draft == False).count()
        
        print(f"Draft articles: {draft_count}")
        print(f"Published articles: {published_count}")
        print()
        
        # Show recent articles
        if total_count > 0:
            print("Recent articles:")
            print("-" * 60)
            articles = session.query(News).order_by(News.created_at.desc()).limit(5).all()
            for article in articles:
                status = "DRAFT" if article.draft else "PUBLISHED"
                print(f"  [{status}] {article.news_title}")
            print()
        
        print("=" * 60)
        print("✅ Database test completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
