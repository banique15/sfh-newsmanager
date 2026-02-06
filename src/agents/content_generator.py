"""Content Generator Agent - Specialized agent for generating article content."""

from crewai import Agent
from src.config.llm import get_llm
from src.tools.content import generate_content


def create_content_generator_agent() -> Agent:
    """
    Create a specialized agent that ONLY generates content.
    This agent has ONE JOB: call Generate Content tool with the provided information.
    """
    
    backstory = """You are a Content Generation Specialist.

YOUR ONLY JOB:
When given a topic or source material, you MUST:
1. IMMEDIATELY call the 'Generate Content' tool
2. Extract the topic and key details from the input
3. Pass them to the Generate Content tool
4. Return the generated content as your final answer

YOU MUST NOT:
- Say "I will generate" or "Let me help" - JUST DO IT
- Ask questions or make small talk
- Return anything other than generated content

EXAMPLE:
Input: "Write an article about Harmony Garden opening"
Your action: Call generate_content(topic="Harmony Garden opening", ...)
Your output: The actual generated article content from the tool

Remember: You are a TOOL EXECUTOR. Execute the Generate Content tool immediately."""

    agent = Agent(
        role="Content Generator",
        goal="Generate article content using the Generate Content tool",
        backstory=backstory,
        tools=[generate_content],  # ONLY this tool
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        max_iter=3,  # Should finish in 1-2 iterations
    )
    
    return agent


# Global instance
content_generator_agent = create_content_generator_agent()
