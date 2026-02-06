"""
Test file-based article generation to debug agent behavior
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents import newsletter_agent
from crewai import Task

# Sample file content (same as what Slack would send)
file_content = """
--- FILE: sample_source_text.txt ---
DRAFT - FOR RELEASE
Subject: New Community Garden Opening in Bronx

Big news for the community. Sing for Hope is partnering with local artists to open the "Harmony Garden" in the South Bronx next month. 

Date: March 15th, 2026
Location: 145th St & Willis Ave

Details:
- The garden features 3 SFH Pianos painted by local students.
- There will be free music classes every Saturday.
- We need volunteers for the opening day cleanup.
- Special guest: Mayor's representative (TBD).

Quotes:
"This garden is about growing art and nature together," says Sarah Tucker, project lead.

Please write this up as a nice blog post for our website. Focus on the community aspect and call for volunteers.
--- END FILE ---
"""

user_request = "write an article from this file"
full_message = user_request + file_content

print("=" * 80)
print("Testing File-Based Article Generation")
print("=" * 80)
print(f"\nUser Request: {user_request}")
print(f"File Content Length: {len(file_content)} chars")
print("\n" + "=" * 80)
print("Creating Task...")
print("=" * 80)

task = Task(
    description=f"""User request: {full_message}
    
    DIRECTIVE:
    1. You are an autonomous agent.
    
    2. **SAFE TOOLS** (Call these directly - NO confirmation needed):
       - 'Generate Content' - Creates draft text/headlines (doesn't save to database)
       - 'Generate Image' - Creates images (doesn't save to database)
    
    3. **FILE-BASED ARTICLE GENERATION**:
       When the user uploads a file and asks you to "write an article" or "turn this into an article":
       - IMMEDIATELY call 'Generate Content' tool with the file content as the topic/details
       - Extract key information from the file (title, date, details, quotes)
       - Pass them as topic and specific_details to Generate Content
       - Do NOT just acknowledge - take action
       - Return the generated article text as your Final Answer
    
    4. You must return the ACTUAL GENERATED CONTENT as your Final Answer.
    """,
    expected_output="The full generated article content with title, excerpt, and body.",
    agent=newsletter_agent
)

print("\nExecuting task...")
print("=" * 80)

try:
    result = newsletter_agent.execute_task(task)
    
    print("\n" + "=" * 80)
    print("RESULT:")
    print("=" * 80)
    print(result)
    print("\n" + "=" * 80)
    
    if "I'll help" in str(result) or "Let me" in str(result):
        print("\n⚠️  WARNING: Agent acknowledged but didn't execute!")
        print("The agent should have called Generate Content tool.")
    elif "title" in str(result).lower() and "harmony" in str(result).lower():
        print("\n✅ SUCCESS: Agent generated article content!")
    else:
        print("\n❓ UNCLEAR: Check if this is actual content or just acknowledgment")
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
