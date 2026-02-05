"""Article search and listing tool for CrewAI."""

from typing import Any, Literal

from crewai.tools import tool
from supabase import create_client

from src.config.settings import settings


def get_supabase():
    """Get Supabase client."""
    return create_client(settings.supabase_url, settings.supabase_key)


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
    try:
        supabase = get_supabase()
        
        # Start query
        query = supabase.table("news").select("*", count="exact")
        
        # Filter by status
        if status == "draft":
            query = query.eq("draft", True)
        elif status == "published":
            query = query.eq("draft", False)
        
        # Search by keyword
        if keyword:
            # Using ilike for case-insensitive search
            # Note: logical OR in PostgREST is done via .or_() filter or raw string
            # We'll use a simpler approach: direct filter if keyword provided
            # For complex OR search (title OR content), we use the .or_ syntax:
            # filter.or_(f"news_title.ilike.%{keyword}%,newscontent.ilike.%{keyword}%")
            search_filter = f"news_title.ilike.%{keyword}%,newscontent.ilike.%{keyword}%"
            query = query.or_(search_filter)
        
        # Ordering
        query = query.order("created_at", desc=True)
        
        # Limits
        limit = min(limit, 100)
        query = query.range(offset, offset + limit - 1)
        
        result = query.execute()
        
        return {
            "success": True,
            "articles": result.data,
            "count": len(result.data),
            "total": result.count,
            "limit": limit,
            "offset": offset,
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to search articles: {str(e)}",
        }


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
    # Call the run method of the tool since it's decorated
    return search_articles.run(keyword=None, status=status, limit=limit, offset=0)


__all__ = ["search_articles", "list_articles"]
