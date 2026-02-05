"""Article CRUD operations tool for CrewAI."""

from datetime import datetime
from typing import Any

from crewai.tools import tool
from supabase import create_client

from src.config.settings import settings


def get_supabase():
    """Get Supabase client."""
    return create_client(settings.supabase_url, settings.supabase_key)


@tool("Create Article")
def create_article(
    news_title: str,
    newscontent: str,
    news_excerpt: str | None = None,
    news_image: str | None = None,
    news_image_caption: str | None = None,
    news_author: str | None = "Newsletter Manager Bot",
    draft: bool = True,
) -> dict[str, Any]:
    """
    Create a new article.
    
    Args:
        news_title: Article title (required)
        newscontent: Article content in HTML (required)
        news_excerpt: Short summary (auto-generated if not provided)
        news_image: URL to hero image
        news_image_caption: Caption for hero image
        news_author: Author name (defaults to 'Newsletter Manager Bot')
        draft: Whether article is draft (default: True)
    
    Returns:
        Dictionary with article data including ID
    """
    try:
        supabase = get_supabase()
        
        data = {
            "news_title": news_title,
            "newscontent": newscontent,
            "news_excerpt": news_excerpt,
            "news_image": news_image,
            "news_image_caption": news_image_caption,
            "news_author": news_author,
            "news_date": datetime.utcnow().isoformat(),
            "draft": draft,
            "created_at": datetime.utcnow().isoformat(),
        }
        
        result = supabase.table("news").insert(data).execute()
        
        if not result.data:
            raise Exception("No data returned from insert")
            
        article = result.data[0]
        
        return {
            "success": True,
            "article": article,
            "message": f"Created article '{article['news_title']}' (ID: {article['id']})",
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to create article: {str(e)}",
        }


@tool("Read Article")
def read_article(article_id: int | None = None, news_url: str | None = None) -> dict[str, Any]:
    """
    Read an article by ID or URL slug.
    
    Args:
        article_id: Article ID
        news_url: Article URL slug
    
    Returns:
        Dictionary with article data
    """
    if not article_id and not news_url:
        return {
            "success": False,
            "error": "Must provide either article_id or news_url",
        }
    
    try:
        supabase = get_supabase()
        query = supabase.table("news").select("*")
        
        if article_id:
            query = query.eq("id", article_id)
        else:
            query = query.eq("news_url", news_url)
            
        result = query.execute()
        
        if not result.data:
            return {
                "success": False,
                "error": "Article not found",
                "message": f"No article found with {'ID: ' + str(article_id) if article_id else 'URL: ' + news_url}",
            }
        
        return {
            "success": True,
            "article": result.data[0],
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to read article: {str(e)}",
        }


@tool("Update Article")
def update_article(
    article_id: int,
    news_title: str | None = None,
    newscontent: str | None = None,
    news_excerpt: str | None = None,
    news_image: str | None = None,
    news_image_caption: str | None = None,
) -> dict[str, Any]:
    """
    Update an existing article.
    
    Args:
        article_id: Article ID (required)
        news_title: New title
        newscontent: New content
        news_excerpt: New excerpt
        news_image: New hero image URL
        news_image_caption: New image caption
    
    Returns:
        Dictionary with updated article data
    """
    try:
        supabase = get_supabase()
        
        # Prepare update data
        data = {}
        if news_title is not None:
            data["news_title"] = news_title
        if newscontent is not None:
            data["newscontent"] = newscontent
        if news_excerpt is not None:
            data["news_excerpt"] = news_excerpt
        if news_image is not None:
            data["news_image"] = news_image
        if news_image_caption is not None:
            data["news_image_caption"] = news_image_caption
            
        if not data:
            return {
                "success": False,
                "error": "No fields to update",
                "message": "No fields provided to update",
            }

        # Automatically update news_updated timestamp
        data["news_updated"] = datetime.utcnow().isoformat()
        
        result = supabase.table("news").update(data).eq("id", article_id).execute()
        
        if not result.data:
            return {
                "success": False,
                "error": "Article not found",
                "message": f"No article found with ID: {article_id}",
            }
            
        article = result.data[0]
        
        return {
            "success": True,
            "article": article,
            "message": f"Updated article '{article['news_title']}' (ID: {article['id']})",
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to update article: {str(e)}",
        }


@tool("Delete Article")
def delete_article(article_id: int) -> dict[str, Any]:
    """
    Permanently delete an article.
    
    Args:
        article_id: Article ID (required)
    
    Returns:
        Dictionary with deletion confirmation
    """
    try:
        supabase = get_supabase()
        
        # Check if exists first to get title
        check = supabase.table("news").select("news_title").eq("id", article_id).execute()
        if not check.data:
            return {
                "success": False,
                "error": "Article not found",
                "message": f"No article found with ID: {article_id}",
            }
            
        title = check.data[0]["news_title"]
        
        # Delete
        supabase.table("news").delete().eq("id", article_id).execute()
        
        return {
            "success": True,
            "message": f"Deleted article '{title}' (ID: {article_id})",
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to delete article: {str(e)}",
        }


@tool("Publish Article")
def publish_article(article_id: int) -> dict[str, Any]:
    """
    Publish an article (set draft=False).
    
    Args:
        article_id: Article ID (required)
    
    Returns:
        Dictionary with published article data
    """
    try:
        supabase = get_supabase()
        
        # Check current status
        check = supabase.table("news").select("draft, news_title").eq("id", article_id).execute()
        if not check.data:
            return {
                "success": False,
                "error": "Article not found",
                "message": f"No article found with ID: {article_id}",
            }
            
        article = check.data[0]
        if not article["draft"]:
            return {
                "success": False,
                "error": "Already published",
                "message": f"Article '{article['news_title']}' is already published",
            }
            
        # Update
        result = supabase.table("news").update({"draft": False}).eq("id", article_id).execute()
        updated_article = result.data[0]
        
        return {
            "success": True,
            "article": updated_article,
            "message": f"Published article '{updated_article['news_title']}' (ID: {article_id})",
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to publish article: {str(e)}",
        }


@tool("Unpublish Article")
def unpublish_article(article_id: int) -> dict[str, Any]:
    """
    Unpublish an article (set draft=True).
    
    Args:
        article_id: Article ID (required)
    
    Returns:
        Dictionary with unpublished article data
    """
    try:
        supabase = get_supabase()
        
        # Check current status
        check = supabase.table("news").select("draft, news_title").eq("id", article_id).execute()
        if not check.data:
            return {
                "success": False,
                "error": "Article not found",
                "message": f"No article found with ID: {article_id}",
            }
            
        article = check.data[0]
        if article["draft"]:
            return {
                "success": False,
                "error": "Already draft",
                "message": f"Article '{article['news_title']}' is already a draft",
            }
            
        # Update
        result = supabase.table("news").update({"draft": True}).eq("id", article_id).execute()
        updated_article = result.data[0]
        
        return {
            "success": True,
            "article": updated_article,
            "message": f"Unpublished article '{updated_article['news_title']}' (ID: {article_id})",
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to unpublish article: {str(e)}",
        }


# Export all tools
__all__ = [
    "create_article",
    "read_article",
    "update_article",
    "delete_article",
    "publish_article",
    "unpublish_article",
]
