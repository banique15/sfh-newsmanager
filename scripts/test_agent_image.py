"""Test script for agent image generation."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from crewai import Task
from src.agents import newsletter_agent


def test_agent_image() -> None:
    """Test agent generating an image from a request."""
    print("\n" + "=" * 60)
    print("TEST: Agent Image Generation Workflow")
    print("=" * 60)
    
    # Request that requires image generation
    task = Task(
        description="Create a hero image for an article about a summer music concert in the park. Make it vibrant and joyful. YOU MUST USE THE 'Generate Image' TOOL. Do not just describe what you will do. Execute it and return the URL.",
        expected_output="The image URL returned by the tool",
        agent=newsletter_agent,
    )
    
    result = newsletter_agent.execute_task(task)
    print("\n✅ Result:")
    print(result)


def main() -> None:
    """Run tests."""
    print("=" * 60)
    print("Agent Image Generation Test")
    print("=" * 60)
    
    try:
        test_agent_image()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
