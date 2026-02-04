"""Simple Supabase connection test."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import settings
from supabase import create_client


def main() -> None:
    """Test Supabase connection."""
    print("=" * 60)
    print("Supabase Connection Test")
    print("=" * 60)
    
    print(f"\nSupabase URL: {settings.supabase_url}")
    print(f"Has Key: {'Yes' if settings.supabase_key else 'No'}")
    
    try:
        # Create Supabase client
        supabase = create_client(settings.supabase_url, settings.supabase_key)
        
        # Test query
        print("\n✅ Supabase client created successfully!")
        
        # Try to query the news table
        result = supabase.table("news").select("id, title").limit(5).execute()
        
        print(f"✅ Successfully queried news table!")
        print(f"✅ Found {len(result.data)} articles")
        
        if result.data:
            print("\nSample articles:")
            for article in result.data:
                print(f"  - [{article['id']}] {article['title']}")
        
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
