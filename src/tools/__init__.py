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
from src.tools.image import generate_image
from src.tools.intent import ask_clarification
from src.tools.slack import slack_tool

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
    generate_image,
    slack_tool,
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
    "generate_image",
    "slack_tool",
    "ALL_TOOLS",
]
