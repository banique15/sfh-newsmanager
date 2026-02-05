"""Test script for agent content generation."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from crewai import Task
from src.agents import newsletter_agent


def test_agent_generation() -> None:
    """Test agent generating an article from a request."""
    print("\n" + "=" * 60)
    print("TEST: Agent Content Generation Workflow")
    print("=" * 60)
    
    # Request that requires generation
    task = Task(
        description="Write a short article about our new volunteer program starting next week. It's for high school students.",
        expected_output="Final answer with the generated content",
        agent=newsletter_agent,
    )
    
    result = newsletter_agent.execute_task(task)
    print("\n✅ Result:")
    print(result)


def main() -> None:
    """Run tests."""
    print("=" * 60)
    print("Agent Content Generation Test")
    print("=" * 60)
    
    try:
        test_agent_generation()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
