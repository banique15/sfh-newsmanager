"""Test script for content generation."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.tools.content import generate_content


def test_generation() -> None:
    """Test generating an article."""
    print("\n" + "=" * 60)
    print("TEST: Generate Content")
    print("=" * 60)
    
    result = generate_content.run(
        topic="New Piano Donation Program",
        tone="inspiring",
        length="short",
        specific_details=["Program starts next month", "50 pianos available"]
    )
    
    print("\n✅ Result:")
    print(result)


def main() -> None:
    """Run tests."""
    print("=" * 60)
    print("Content Generation Tool Test")
    print("=" * 60)
    
    try:
        test_generation()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
