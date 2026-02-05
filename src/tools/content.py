"""Content generation tools for CrewAI."""

import json
from typing import Any

from crewai.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from src.config.settings import settings


@tool("Generate Content")
def generate_content(
    topic: str,
    tone: str = "inspiring",
    length: str = "medium",
    specific_details: list[str] | None = None,
) -> dict[str, Any]:
    """
    Generate article content (headline, body, excerpt) using AI.
    
    Args:
        topic: Main subject of the article
        tone: Tone of writing (default: 'inspiring')
        length: Article length - 'short', 'medium', 'long' (default: 'medium')
        specific_details: Optional list of facts or details to include
    
    Returns:
        Dictionary with title, content, and excerpt
    """
    # Create a dedicated LLM client for generation to ensure correct model name
    # (CrewAI needs a prefix that OpenRouter rejects)
    model = settings.default_model
    if model.startswith("openrouter/"):
        model = model.replace("openrouter/", "")
        
    llm = ChatOpenAI(
        model=model,
        api_key=settings.openai_api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.7,
        default_headers={
            "HTTP-Referer": "https://github.com/singforhope/newsletter-manager",
            "X-Title": "Newsletter Manager",
        },
    )
    
    # Construct details string
    details_str = ""
    if specific_details:
        details_str = "\n".join([f"- {detail}" for detail in specific_details])
    else:
        details_str = "None provided"

    # prompt template from examples/prompts/article_generation.md
    prompt_text = f"""Create a news article about: {topic}

Requirements:
- Tone: {tone}
- Target audience: Sing for Hope staff, donors, volunteers, community members
- Length: {length}
- Include specific details:
{details_str}

Generate:
1. A compelling headline (5-10 words)
2. A short excerpt/summary (1-2 sentences, ~30-50 words)
3. Full article body with:
   - Engaging opening
   - Key details and context
   - Call to action or closing thought
   - Use markdown formatting for structure (headers, lists, bold)

IMPORTANT: Return valid JSON only, with no markdown code blocks.
Format:
{{
  "title": "Generated headline here",
  "excerpt": "Generated excerpt here",
  "content": "Full article content here with markdown formatting"
}}
"""

    messages = [
        SystemMessage(content="You are a professional content writer for Sing for Hope, a nonprofit bringing arts to communities."),
        HumanMessage(content=prompt_text)
    ]
    
    try:
        response = llm.invoke(messages)
        content = response.content
        
        # Clean potential markdown formatting from LLM
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "")
        elif content.startswith("```"):
            content = content.replace("```", "")
            
        result = json.loads(content.strip())
        
        return {
            "success": True,
            "data": result,
            "message": f"Generated content for '{topic}'"
        }
        
    except json.JSONDecodeError:
        return {
            "success": False,
            "error": "JSON Parse Error",
            "message": "Failed to parse AI response. Raw output: " + str(response.content)[:200]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to generate content: {str(e)}"
        }


__all__ = ["generate_content"]
