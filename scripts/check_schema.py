"""Check what columns exist in the news table."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import settings
from supabase import create_client


def main() -> None:
    """Check news table schema."""
    print("=" * 60)
    print("Checking News Table Schema")
    print("=" * 60)
    
    try:
        # Create Supabase client
        supabase = create_client(settings.supabase_url, settings.supabase_key)
        
        print("\n✅ Connected to Supabase")
        
        # Try to get any row to see the schema
        print("\nFetching one row to see schema...")
        result = supabase.table("news").select("*").limit(1).execute()
        
        if result.data:
            print(f"\n✅ Found {len(result.data)} row(s)")
            print("\nColumns in the news table:")
            for key in result.data[0].keys():
                print(f"  - {key}")
            
            print("\nSample data:")
            import json
            print(json.dumps(result.data[0], indent=2, default=str))
        else:
            print("\n⚠️  Table exists but is empty")
            print("Run migrations to create the schema and seed data")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
