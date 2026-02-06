"""
Simplified test bypassing circular imports
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test calling content generation API directly
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from src.config.settings import settings
import json

print("="*80)
print("Testing Content Generation API Directly")
print("="*80)

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

topic = "Harmony Garden Opening in South Bronx"
details = [
    "Sing for Hope partnering with local artists",
    "Opening March 15th, 2026 at 145th St & Willis Ave",
    "Features 3 SFH Pianos painted by local students"
]

details_str = "\n".join([f"- {d}" for d in details])

prompt = f"""Create a news article about: {topic}

Requirements:
- Tone: inspiring
- Length: medium
- Include specific details:
{details_str}

Generate:
1. A compelling headline (5-10 words)
2. A short excerpt (1-2 sentences)
3. Full article body with markdown formatting

IMPORTANT: Return valid JSON only.
Format:
{{
  "title": "Generated headline",
  "excerpt": "Generated excerpt",
  "content": "Full article content"
}}
"""

print("\nCalling LLM...")
print("="*80)

try:
    messages = [
        SystemMessage(content="You are a professional content writer for Sing for Hope."),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    content = response.content
    
    # Clean markdown
    if content.startswith("```json"):
        content = content.replace("```json", "").replace("```", "")
    elif content.startswith("```"):
        content = content.replace("```", "")
    
    result = json.loads(content.strip())
    
    print("\n✅ SUCCESS!")
    print("="*80)
    print(f"Title: {result['title']}")
    print(f"Excerpt: {result['excerpt']}")
    print(f"\nContent ({len(result['content'])} chars):")
    print("-"*80)
    print(result['content'])
    print("-"*80)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
