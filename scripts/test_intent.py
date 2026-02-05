"""Test script for ambiguous requests."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from crewai import Task
from src.agents import newsletter_agent


def test_ambiguous_query() -> None:
    """Test agent with an ambiguous query."""
    print("\n" + "=" * 60)
    print("TEST: Ambiguous Query ('help')")
    print("=" * 60)
    
    task = Task(
        description="help",
        expected_output="A clarification request listing capabilities",
        agent=newsletter_agent,
    )
    
    result = newsletter_agent.execute_task(task)
    print("\n❓ Result:")
    print(result)


def main() -> None:
    """Run tests."""
    print("=" * 60)
    print("Intent Detection Test")
    print("=" * 60)
    
    try:
        test_ambiguous_query()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
