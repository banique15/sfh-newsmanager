"""
Test Generate Content tool directly
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tools.content import generate_content

print("=" * 80)
print("Testing Generate Content Tool Directly")
print("=" * 80)

# Test case: Harmony Garden article
topic = "Harmony Garden Opening in South Bronx"
details = [
    "Sing for Hope partnering with local artists",
    "Opening March 15th, 2026 at 145th St & Willis Ave",
    "Features 3 SFH Pianos painted by local students",
    "Free music classes every Saturday",
    "Need volunteers for opening day cleanup",
    'Quote from Sarah Tucker: "This garden is about growing art and nature together"'
]

print(f"\nTopic: {topic}")
print(f"Details: {len(details)} items")
print("\nCalling generate_content()...")
print("=" * 80)

result = generate_content(
    topic=topic,
    tone="inspiring",
    length="medium",
    specific_details=details
)

print("\n" + "=" * 80)
print("RESULT:")
print("=" * 80)
print(f"Success: {result.get('success')}")

if result.get('success'):
    data = result.get('data', {})
    print(f"\n✅ Title: {data.get('title')}")
    print(f"✅ Excerpt: {data.get('excerpt')}")
    print(f"\n✅ Content ({len(data.get('content', ''))} chars):")
    print("-" * 80)
    print(data.get('content'))
    print("-" * 80)
else:
    print(f"\n❌ Error: {result.get('error')}")
    print(f"Message: {result.get('message')}")
