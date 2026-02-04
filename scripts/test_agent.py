"""Test script for Newsletter Manager agent."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from crewai import Task

from src.agents import newsletter_agent


def test_simple_query() -> None:
    """Test agent with a simple query."""
    print("\n" + "=" * 60)
    print("TEST: Simple Article Listing Query")
    print("=" * 60)
    
    task = Task(
        description="List all draft articles",
        expected_output="A list of draft articles with their titles and IDs",
        agent=newsletter_agent,
    )
    
    result = newsletter_agent.execute_task(task)
    print("\n📋 Result:")
    print(result)


def test_create_article() -> None:
    """Test agent creating an article."""
    print("\n" + "=" * 60)
    print("TEST: Create Article")
    print("=" * 60)
    
    task = Task(
        description="""Create a new draft article with the following:
        Title: "Test Article from AI Agent"
        Content: "This is a test article created by the Newsletter Manager AI agent to verify the system is working correctly."
        Author: "AI Agent Test"
        """,
        expected_output="Confirmation that the article was created with its ID",
        agent=newsletter_agent,
    )
    
    result = newsletter_agent.execute_task(task)
    print("\n✅ Result:")
    print(result)


def test_natural_query() -> None:
    """Test agent with natural language."""
    print("\n" + "=" * 60)
    print("TEST: Natural Language Query")
    print("=" * 60)
    
    task = Task(
        description="Show me what articles we have about pianos",
        expected_output="Search results for articles about pianos",
        agent=newsletter_agent,
    )
    
    result = newsletter_agent.execute_task(task)
    print("\n🔍 Result:")
    print(result)


def main() -> None:
    """Run agent tests."""
    print("=" * 60)
    print("Newsletter Manager Agent - Test Suite")
    print("=" * 60)
    
    try:
        # Test 1: Simple query
        test_simple_query()
        
        # Test 2: Create article
        test_create_article()
        
        # Test 3: Natural language
        test_natural_query()
        
        print("\n" + "=" * 60)
        print("✅ All agent tests completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
