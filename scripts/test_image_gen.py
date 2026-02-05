"""Test script for image generation."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.tools.image import generate_image


def test_image_gen() -> None:
    """Test generating an image."""
    print("\n" + "=" * 60)
    print("TEST: Generate Image")
    print("=" * 60)
    
    result = generate_image.run(
        description="A group of diverse children singing together in a park",
        style="vibrant",
        mood="joyful"
    )
    
    print("\n✅ Result:")
    print(result)


def main() -> None:
    """Run tests."""
    print("=" * 60)
    print("Image Generation Tool Test")
    print("=" * 60)
    
    try:
        test_image_gen()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
