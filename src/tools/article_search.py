"""Article search and listing tool for CrewAI."""

from typing import Any, Literal

from crewai.tools import tool
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.database import News, get_db


@tool("Search Articles")
def search_articles(
    keyword: str | None = None,
    status: Literal["draft", "published", "all"] = "all",
    limit: int = 20,
    offset: int = 0,
) -> dict[str, Any]:
    """
    Search and list articles.
    
    Args:
        keyword: Search in title and content (optional)
        status: Filter by status - 'draft', 'published', or 'all' (default: 'all')
        limit: Maximum number of results (default: 20, max: 100)
        offset: Number of results to skip (default: 0)
    
    Returns:
        Dictionary with articles list and count
    """
    session: Session = next(get_db())
    
    try:
        # Build query
        query = session.query(News)
        
        # Filter by status
        if status == "draft":
            query = query.filter(News.draft == True)
        elif status == "published":
            query = query.filter(News.draft == False)
        
        # Search by keyword
        if keyword:
            search_pattern = f"%{keyword}%"
            query = query.filter(
                or_(
                    News.news_title.ilike(search_pattern),
                    News.newscontent.ilike(search_pattern),
                    News.news_excerpt.ilike(search_pattern),
                )
            )
        
        # Get total count
        total_count = query.count()
        
        # Apply limit and offset
        limit = min(limit, 100)  # Cap at 100
        articles = query.order_by(News.created_at.desc()).limit(limit).offset(offset).all()
        
        return {
            "success": True,
            "articles": [article.to_dict() for article in articles],
            "count": len(articles),
            "total": total_count,
            "limit": limit,
            "offset": offset,
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to search articles: {str(e)}",
        }
    finally:
        session.close()


@tool("List Articles")
def list_articles(
    status: Literal["draft", "published", "all"] = "all",
    limit: int = 10,
) -> dict[str, Any]:
    """
    List recent articles.
    
    Args:
        status: Filter by status - 'draft', 'published', or 'all' (default: 'all')
        limit: Maximum number of results (default: 10)
    
    Returns:
        Dictionary with articles list
    """
    return search_articles(keyword=None, status=status, limit=limit, offset=0)


__all__ = ["search_articles", "list_articles"]
