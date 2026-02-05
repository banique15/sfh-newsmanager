"""Image generation tools for CrewAI."""

from typing import Any

from crewai.tools import tool
from openai import OpenAI

from src.config.settings import settings


def get_image_client() -> OpenAI:
    """Get OpenAI client configured for OpenRouter."""
    return OpenAI(
        api_key=settings.openai_api_key,
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "https://github.com/singforhope/newsletter-manager",
            "X-Title": "Newsletter Manager",
        },
    )


@tool("Generate Image")
def generate_image(
    description: str,
    style: str = "vibrant",
    mood: str = "inspiring",
    aspect_ratio: str = "16:9",
) -> dict[str, Any]:
    """
    Generate an image using AI (DALL-E 3).
    
    Args:
        description: Description of what the image should show
        style: Visual style (e.g., vibrant, elegant, minimalist)
        mood: Emotional tone (e.g., inspiring, joyful)
        aspect_ratio: Aspect ratio (default: 16:9)
    
    Returns:
        Dictionary with image URL and metadata
    """
    try:
        client = get_image_client()
        
        # Construct full prompt
        full_prompt = (
            f"Generate a {style} and {mood} image suitable for a nonprofit newsletter. "
            f"Subject: {description}. "
            "High quality, professional, artistic."
        )
        
        # OpenRouter Image Generation via Chat Completions
        # Using Flux model which supports text-to-image via chat endpoint
        # Trying flux-1-dev as schnell might be deprecated or restricted
        model = "black-forest-labs/flux-1-dev"
        
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": full_prompt}
                ],
            )
            
            # The image URL is usually returned in the content content
            content = response.choices[0].message.content
            image_url = ""
            
            # Extract URL (simple markdown link extraction or identifying http)
            import re
            url_match = re.search(r'\((https?://[^\s)]+)\)', content) # Look for markdown like [](url)
            if url_match:
                image_url = url_match.group(1)
            else:
                # Look for raw URL
                url_match = re.search(r'(https?://[^\s]+)', content)
                if url_match:
                    image_url = url_match.group(1)
                else:
                    image_url = content
                    
        except Exception as api_error:
            # Fallback to placeholder if API fails (e.g. model not available)
            print(f"Image API failed: {api_error}. Using fallback.")
            import urllib.parse
            encoded_desc = urllib.parse.quote(description)
            image_url = f"https://placehold.co/1024x576?text={encoded_desc}"
            model = "placeholder (fallback)"
        
        return {
            "success": True,
            "image_url": image_url,
            "description": full_prompt,
            "message": f"Generated image for '{description}'",
            "metadata": {
                "style": style,
                "mood": mood,
                "model": model
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to generate image: {str(e)}"
        }


__all__ = ["generate_image"]
