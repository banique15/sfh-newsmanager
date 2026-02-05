"""Intent detection and clarification tools."""

from typing import Any

from crewai.tools import tool


@tool("Ask Clarification")
def ask_clarification(
    question: str,
    options: list[str] | None = None,
    examples: list[str] | None = None,
) -> dict[str, Any]:
    """
    Ask the user for clarification when a request is ambiguous.
    
    Args:
        question: The specific question to ask
        options: Optional list of valid options or choices
        examples: Optional list of example valid inputs
    
    Returns:
        Dictionary containing the formatted clarification request
    """
    message = f"❓ {question}"
    
    if options:
        message += "\n\nOptions:"
        for opt in options:
            message += f"\n- {opt}"
            
    if examples:
        message += "\n\nExamples:"
        for ex in examples:
            message += f"\n- {ex}"
            
    # This return value is intended to be shown to the user
    # In a real agent loop, this would trigger a pause or specific UI response
    return {
        "success": True,
        "requires_user_input": True,
        "message": message,
        "type": "clarification",
    }


__all__ = ["ask_clarification"]
