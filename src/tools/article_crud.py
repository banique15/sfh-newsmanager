"""Article CRUD operations tool for CrewAI."""

from datetime import datetime
from typing import Any, Literal

from crewai.tools import tool
from sqlalchemy.orm import Session

from src.database import News, get_db


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
    session: Session = next(get_db())
    
    try:
        # Create article instance
        article = News(
            news_title=news_title,
            newscontent=newscontent,
            news_excerpt=news_excerpt,
            news_image=news_image,
            news_image_caption=news_image_caption,
            news_author=news_author,
            news_date=datetime.utcnow(),
            draft=draft,
        )
        
        session.add(article)
        session.commit()
        session.refresh(article)
        
        return {
            "success": True,
            "article": article.to_dict(),
            "message": f"Created article '{article.news_title}' (ID: {article.id})",
        }
        
    except Exception as e:
        session.rollback()
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to create article: {str(e)}",
        }
    finally:
        session.close()


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
    
    session: Session = next(get_db())
    
    try:
        query = session.query(News)
        
        if article_id:
            article = query.filter(News.id == article_id).first()
        else:
            article = query.filter(News.news_url == news_url).first()
        
        if not article:
            return {
                "success": False,
                "error": "Article not found",
                "message": f"No article found with {'ID: ' + str(article_id) if article_id else 'URL: ' + news_url}",
            }
        
        return {
            "success": True,
            "article": article.to_dict(),
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to read article: {str(e)}",
        }
    finally:
        session.close()


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
    session: Session = next(get_db())
    
    try:
        article = session.query(News).filter(News.id == article_id).first()
        
        if not article:
            return {
                "success": False,
                "error": "Article not found",
                "message": f"No article found with ID: {article_id}",
            }
        
        # Update fields if provided
        if news_title is not None:
            article.news_title = news_title
        if newscontent is not None:
            article.newscontent = newscontent
        if news_excerpt is not None:
            article.news_excerpt = news_excerpt
        if news_image is not None:
            article.news_image = news_image
        if news_image_caption is not None:
            article.news_image_caption = news_image_caption
        
        # news_updated is auto-set by trigger
        session.commit()
        session.refresh(article)
        
        return {
            "success": True,
            "article": article.to_dict(),
            "message": f"Updated article '{article.news_title}' (ID: {article.id})",
        }
        
    except Exception as e:
        session.rollback()
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to update article: {str(e)}",
        }
    finally:
        session.close()


@tool("Delete Article")
def delete_article(article_id: int) -> dict[str, Any]:
    """
    Permanently delete an article.
    
    Args:
        article_id: Article ID (required)
    
    Returns:
        Dictionary with deletion confirmation
    """
    session: Session = next(get_db())
    
    try:
        article = session.query(News).filter(News.id == article_id).first()
        
        if not article:
            return {
                "success": False,
                "error": "Article not found",
                "message": f"No article found with ID: {article_id}",
            }
        
        title = article.news_title
        session.delete(article)
        session.commit()
        
        return {
            "success": True,
            "message": f"Deleted article '{title}' (ID: {article_id})",
        }
        
    except Exception as e:
        session.rollback()
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to delete article: {str(e)}",
        }
    finally:
        session.close()


@tool("Publish Article")
def publish_article(article_id: int) -> dict[str, Any]:
    """
    Publish an article (set draft=False).
    
    Args:
        article_id: Article ID (required)
    
    Returns:
        Dictionary with published article data
    """
    session: Session = next(get_db())
    
    try:
        article = session.query(News).filter(News.id == article_id).first()
        
        if not article:
            return {
                "success": False,
                "error": "Article not found",
                "message": f"No article found with ID: {article_id}",
            }
        
        if not article.draft:
            return {
                "success": False,
                "error": "Already published",
                "message": f"Article '{article.news_title}' is already published",
            }
        
        article.draft = False
        session.commit()
        session.refresh(article)
        
        return {
            "success": True,
            "article": article.to_dict(),
            "message": f"Published article '{article.news_title}' (ID: {article.id})",
        }
        
    except Exception as e:
        session.rollback()
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to publish article: {str(e)}",
        }
    finally:
        session.close()


@tool("Unpublish Article")
def unpublish_article(article_id: int) -> dict[str, Any]:
    """
    Unpublish an article (set draft=True).
    
    Args:
        article_id: Article ID (required)
    
    Returns:
        Dictionary with unpublished article data
    """
    session: Session = next(get_db())
    
    try:
        article = session.query(News).filter(News.id == article_id).first()
        
        if not article:
            return {
                "success": False,
                "error": "Article not found",
                "message": f"No article found with ID: {article_id}",
            }
        
        if article.draft:
            return {
                "success": False,
                "error": "Already draft",
                "message": f"Article '{article.news_title}' is already a draft",
            }
        
        article.draft = True
        session.commit()
        session.refresh(article)
        
        return {
            "success": True,
            "article": article.to_dict(),
            "message": f"Unpublished article '{article.news_title}' (ID: {article.id})",
        }
        
    except Exception as e:
        session.rollback()
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to unpublish article: {str(e)}",
        }
    finally:
        session.close()


# Export all tools
__all__ = [
    "create_article",
    "read_article",
    "update_article",
    "delete_article",
    "publish_article",
    "unpublish_article",
]
