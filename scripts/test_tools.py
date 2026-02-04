"""Test script for article CRUD tools."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.tools import (
    create_article,
    delete_article,
    list_articles,
    publish_article,
    read_article,
    search_articles,
    update_article,
)


def test_create_article() -> None:
    """Test creating an article."""
    print("\n" + "=" * 60)
    print("TEST: Create Article")
    print("=" * 60)
    
    result = create_article.run(
        news_title="Test Article from Script",
        newscontent="<p>This is a test article created from the test script.</p>",
        news_author="Test Script",
        draft=True,
    )
    
    print(result)
    
    if result.get("success"):
        print(f"✅ Created article ID: {result['article']['id']}")
        return result['article']['id']
    else:
        print(f"❌ Failed: {result.get('error')}")
        return None


def test_read_article(article_id: int) -> None:
    """Test reading an article."""
    print("\n" + "=" * 60)
    print(f"TEST: Read Article (ID: {article_id})")
    print("=" * 60)
    
    result = read_article.run(article_id=article_id)
    
    if result.get("success"):
        article = result['article']
        print(f"✅ Found article: {article['news_title']}")
        print(f"   Status: {'DRAFT' if article['draft'] else 'PUBLISHED'}")
    else:
        print(f"❌ Failed: {result.get('error')}")


def test_update_article(article_id: int) -> None:
    """Test updating an article."""
    print("\n" + "=" * 60)
    print(f"TEST: Update Article (ID: {article_id})")
    print("=" * 60)
    
    result = update_article.run(
        article_id=article_id,
        news_title="Updated Test Article",
    )
    
    if result.get("success"):
        print(f"✅ Updated article: {result['article']['news_title']}")
    else:
        print(f"❌ Failed: {result.get('error')}")


def test_search_articles() -> None:
    """Test searching articles."""
    print("\n" + "=" * 60)
    print("TEST: Search Articles")
    print("=" * 60)
    
    result = search_articles.run(keyword="test", status="all", limit=5)
    
    if result.get("success"):
        print(f"✅ Found {result['count']} articles (total: {result['total']})")
        for article in result['articles']:
            status = "DRAFT" if article['draft'] else "PUBLISHED"
            print(f"   [{status}] {article['news_title']}")
    else:
        print(f"❌ Failed: {result.get('error')}")


def test_list_articles() -> None:
    """Test listing articles."""
    print("\n" + "=" * 60)
    print("TEST: List Articles")
    print("=" * 60)
    
    # List drafts
    result = list_articles.run(status="draft", limit=5)
    
    if result.get("success"):
        print(f"✅ Found {result['count']} draft articles")
        for article in result['articles']:
            print(f"   [DRAFT] {article['news_title']}")
    else:
        print(f"❌ Failed: {result.get('error')}")


def test_publish_article(article_id: int) -> None:
    """Test publishing an article."""
    print("\n" + "=" * 60)
    print(f"TEST: Publish Article (ID: {article_id})")
    print("=" * 60)
    
    result = publish_article.run(article_id=article_id)
    
    if result.get("success"):
        print(f"✅ Published: {result['article']['news_title']}")
    else:
        print(f"❌ Failed: {result.get('error')}")


def test_delete_article(article_id: int) -> None:
    """Test deleting an article."""
    print("\n" + "=" * 60)
    print(f"TEST: Delete Article (ID: {article_id})")
    print("=" * 60)
    
    result = delete_article.run(article_id=article_id)
    
    if result.get("success"):
        print(f"✅ Deleted article")
    else:
        print(f"❌ Failed: {result.get('error')}")


def main() -> None:
    """Run all tests."""
    print("=" * 60)
    print("Article CRUD Tools - Test Suite")
    print("=" * 60)
    
    # Test create
    article_id = test_create_article()
    
    if not article_id:
        print("\n❌ Failed to create article, stopping tests")
        return
    
    # Test read
    test_read_article(article_id)
    
    # Test update
    test_update_article(article_id)
    
    # Test search
    test_search_articles()
    
    # Test list
    test_list_articles()
    
    # Test publish
    test_publish_article(article_id)
    
    # Test delete (cleanup)
    test_delete_article(article_id)
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
