"""CrewAI tools package."""

from src.tools.article_crud import (
    create_article,
    delete_article,
    publish_article,
    read_article,
    unpublish_article,
    update_article,
)
from src.tools.article_search import list_articles, search_articles
from src.tools.content import generate_content
from src.tools.intent import ask_clarification

# All available tools
ALL_TOOLS = [
    create_article,
    read_article,
    update_article,
    delete_article,
    publish_article,
    unpublish_article,
    search_articles,
    list_articles,
    ask_clarification,
    generate_content,
]

__all__ = [
    "create_article",
    "read_article",
    "update_article",
    "delete_article",
    "publish_article",
    "unpublish_article",
    "search_articles",
    "list_articles",
    "ask_clarification",
    "generate_content",
    "ALL_TOOLS",
]
