"""Test database connection."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import settings
from supabase import create_client
from supabase import create_client
import traceback


def main() -> None:
    """Test database connection."""
    print("=" * 60)
    print("Newsletter Manager - Database Connection Test")
    print("=" * 60)
    
    print(f"\nSupabase URL: {settings.supabase_url[:30]}...")
    
    try:
        # Test 1: Supabase client connection
        print("\n[Test 1] Creating Supabase client...")
        supabase = create_client(settings.supabase_url, settings.supabase_key)
        print("✅ Supabase client created")
        
        # Test 2: Query news table
        print("\n[Test 2] Querying news table...")
        result = supabase.table("news").select("id, news_title, draft").limit(10).execute()
        total_count = len(result.data)
        print(f"✅ Successfully queried news table")
        print(f"✅ Found {total_count} articles")
        
        # Test 3: Filter by status
        print("\n[Test 3] Filtering by draft status...")
        draft_result = supabase.table("news").select("*", count="exact").eq("draft", True).execute()
        published_result = supabase.table("news").select("*", count="exact").eq("draft", False).execute()
        
        draft_count = draft_result.count if hasattr(draft_result, 'count') else len(draft_result.data)
        published_count = published_result.count if hasattr(published_result, 'count') else len(published_result.data)
        
        print(f"✅ Draft articles: {draft_count}")
        print(f"✅ Published articles: {published_count}")
        
        # Test 4: Display sample articles
        if result.data:
            print("\n[Test 4] Sample articles:")
            for article in result.data[:5]:
                status = "DRAFT" if article.get('draft') else "PUBLISHED"
                print(f"  [{article['id']}] {article['news_title']} ({status})")
        
        print("\n" + "=" * 60)
        print("✅ All database tests passed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return


if __name__ == "__main__":
    main()
