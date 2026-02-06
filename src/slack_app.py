"""
Slack Application Entry Point.
Runs the Slack Bot in Socket Mode using Slack Bolt sdk.
"""

import logging
import os
import re
import json

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError

from src.agents import newsletter_agent
from src.agents.content_generator import content_generator_agent
from src.config.settings import settings
from src.agents.memory import memory
from src.agents.state import state_manager
from crewai import Task

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SlackBot")

# Initialize Bolt App
app = App(
    token=settings.slack_bot_token,
    signing_secret=settings.slack_signing_secret
)

# Event handlers moved below after helper functions

# Preview Button Handler
@app.action("preview_action")
def handle_preview(ack, logger):
    """Handle the View Preview button click."""
    ack()  # Just acknowledge - the URL button handles navigation
    logger.info("👀 Preview button clicked")

@app.action("approve_action")
def handle_approve(ack, body, say):
    """Handle approve button click."""
    ack()
    user_id = body["user"]["id"]
    
    # Get the thread_ts from the message (this is where the confirmation was posted)
    # The message might be in a thread, so check message.thread_ts first
    message = body.get("message", {})
    thread_ts = message.get("thread_ts") or message.get("ts")
    
    logger.info(f"Approve clicked - thread_ts: {thread_ts}")
    
    # 1. Retrieve Pending Action
    action = state_manager.get_pending_action(thread_ts)
    if not action:
        logger.error(f"No pending action found for thread: {thread_ts}")
        say(f"⚠️ No pending action found for this thread (it may have expired or been executed).", thread_ts=thread_ts)
        return

    tool_name = action.get("tool_name")
    tool_args = action.get("tool_args", {})
    
    say(f"✅ Approved by <@{user_id}>! Executing *{tool_name}*...", thread_ts=thread_ts)
    
    # 2. Execute Tool
    # Find the tool function from our registry using case-insensitive match
    target_tool = None
    normalized_name = tool_name.replace(" ", "_").lower()
    
    # Simple mapping for known tools or search in ALL_TOOLS
    from src.tools import ALL_TOOLS
    
    for tool_func in ALL_TOOLS:
        if tool_func.name.replace(" ", "_").lower() == normalized_name:
            target_tool = tool_func
            break
            
    if target_tool:
        try:
            # Execute the tool directly
            # Note: CrewAI tools are callable, arguments passed as kwargs
            result = target_tool._run(**tool_args)
            
            say(f"🎉 **Action Complete**:\n{str(result)}", thread_ts=thread_ts)
            
            # Clear state
            state_manager.clear_pending_action(thread_ts)
            
             # Update memory with the result so conversation flow continues
            memory.add_message(thread_ts, "system", f"Action {tool_name} executed successfully. Result: {result}")
            
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            say(f"❌ Execution failed: {str(e)}", thread_ts=thread_ts)
    else:
        say(f"❌ Error: Could not find tool function for '{tool_name}'", thread_ts=thread_ts)


@app.action("deny_action")
def handle_deny(ack, body, say):
    """Handle deny button click."""
    ack()
    user_id = body["user"]["id"]
    thread_ts = body["container"]["message_ts"]
    
    state_manager.clear_pending_action(thread_ts)
    say(f"🚫 Request denied by <@{user_id}>. Action cancelled.", thread_ts=thread_ts)
    memory.add_message(thread_ts, "system", f"User <@{user_id}> denied the action.")


import httpx
import threading
import uvicorn
from src.dashboard import app as dashboard_app

# ... (Previous imports)

def start_dashboard():
    """Start the dashboard in a separate thread."""
    try:
        uvicorn.run(dashboard_app, host="0.0.0.0", port=8000, log_level="warning")
    except Exception as e:
        logger.error(f"Failed to start dashboard: {e}")

def process_files(files):
    """Download and extract text from Slack files."""
    content = ""
    headers = {"Authorization": f"Bearer {settings.slack_bot_token}"}
    
    for file in files:
        file_type = file.get("filetype")
        url = file.get("url_private")
        name = file.get("name")
        
        if not url:
            continue
            
        logger.info(f"Processing file: {name} ({file_type})")
        
        try:
            # We use httpx to download the file content
            with httpx.Client() as client:
                response = client.get(url, headers=headers, follow_redirects=True)
                
            if response.status_code == 200:
                file_text = response.text
                # Simple text extraction. For PDF, we might need PyPDF (not installed).
                # Supporting text types for now.
                if file_type in ["text", "markdown", "javascript", "python", "json", "csv"]:
                    content += f"\n\n--- FILE: {name} ---\n{file_text}\n--- END FILE ---\n"
                elif file_type == "pdf":
                    # Placeholder for PDF
                    content += f"\n\n[Attached PDF: {name} - (PDF parsing requires extra libraries, showing metadata only)]\n"
                else:
                    content += f"\n\n[Attached File: {name} ({file_type}) - Content skipped]\n"
        except Exception as e:
            logger.error(f"Error downloading file {name}: {e}")
            
    return content

@app.event("app_mention")
def handle_app_mention(event, say):
    """Handle when bot is mentioned (@Newsletter Manager)."""
    channel_id = event["channel"]
    user_id = event["user"]
    text = event["text"]
    thread_ts = event.get("thread_ts", event["ts"])
    ts = event["ts"]
    
    files = event.get("files", [])
    logger.info(f"=== FILE DEBUG === Event has 'files' key: {'files' in event}, Count: {len(files)}")
    
    # Robust File Fetching Strategy
    # 1. Fetch recent history (fetching a batch is more reliable than exact TS matching via API params)
    if not files:
        try:
            logger.info(f"files key missing in event. Fetching history for channel {channel_id} around ts {ts}...")
            # Fetch last 5 messages
            result = app.client.conversations_history(
                channel=channel_id,
                limit=5
            )
            messages = result.get("messages", [])
            
            # Find our message
            target_msg = next((m for m in messages if m["ts"] == ts), None)
            if target_msg:
                files = target_msg.get("files", [])
                if files:
                    logger.info(f"Found {len(files)} files in history for message {ts}")
            
            # 2. Check Parent if in thread and still no files
            if not files and thread_ts != ts:
                # For threads, we might need to fetch the parent specifically if it's old
                # But typically it's in the recent history if the reply is quick. 
                # If not, let's fetch it explicitly.
                logger.info(f"Checking parent message {thread_ts} for files...")
                
                # Check if parent is already in the batch we fetched
                parent_msg = next((m for m in messages if m["ts"] == thread_ts), None)
                
                if not parent_msg:
                    # Fetch specific parent
                    parent_result = app.client.conversations_history(
                        channel=channel_id,
                        latest=thread_ts,
                        inclusive=True,
                        limit=1
                    )
                    parent_messages = parent_result.get("messages", [])
                    if parent_messages:
                        parent_msg = parent_messages[0]
                
                if parent_msg:
                    parent_files = parent_msg.get("files", [])
                    if parent_files:
                        logger.info(f"Found {len(parent_files)} files in parent message.")
                        # Append parent files to the list
                        files.extend(parent_files)
                        
        except Exception as e:
            logger.error(f"Error fetching message history: {e}")

    # Process files if any
    file_context = ""
    if files:
        logger.info(f"=== FILE DEBUG === Processing {len(files)} file(s)")
        say(f"📂 I found {len(files)} file(s). Reading them...", thread_ts=thread_ts)
        file_context = process_files(files)
        logger.info(f"=== FILE DEBUG === File context length: {len(file_context)} chars")
        logger.info(f"=== FILE DEBUG === File context preview: {file_context[:200]}...")
    else:
        logger.info("=== FILE DEBUG === No files found after all attempts")
    
    # Clean text (remove mention)
    text = re.sub(r"<@\w+>", "", text).strip()
    
    if not text and not file_context:
        say("Hello! I'm the Newsletter Manager. How can I help you? try 'help'", thread_ts=thread_ts)
        return

    logger.info(f"Received mention in {channel_id}: {text}")
    
    # 1. Add User Message to History
    # We append file context to the stored message so LLM sees it in history too
    full_message = text + file_context
    memory.add_message(thread_ts, "user", full_message)
    
    # 2. Get Context
    history_context = memory.get_formatted_history(thread_ts)
    
    # Notify user we are working on it
    say(f"👋 Hi <@{user_id}>, I'm looking into that...", thread_ts=thread_ts)
    
    # 3. SPECIAL CASE: If files were uploaded and user wants content generation
    #    Use the specialized content_generator_agent instead of newsletter_agent
    generation_keywords = ["write", "generate", "create", "draft", "article", "turn this into"]
    use_content_agent = file_context and any(keyword in text.lower() for keyword in generation_keywords)
    
    selected_agent = content_generator_agent if use_content_agent else newsletter_agent
    
    if use_content_agent:
        logger.info("🎯 Using specialized Content Generator Agent for file-based generation")
    
    # Run Agent
    try:
        task = Task(
            description=f"""User request from Slack channel {channel_id}: {full_message}
            
            {history_context}
            
            CONTEXT:
            - Channel ID: {channel_id}
            - Thread TS: {thread_ts}
            
            DIRECTIVE:
            1. You are an autonomous agent. 
            
            2. **SAFE TOOLS** (Call these directly - NO confirmation needed):
               - 'Generate Content' - Creates draft text/headlines (doesn't save to database)
               - 'Generate Image' - Creates images (doesn't save to database)
               - 'Search Articles' - Reads from database
               - 'Read Article' - Reads from database
               - 'List Articles' - Reads from database
            
            3. **DESTRUCTIVE TOOLS** (MUST use 'Ask Confirmation' workflow):
               - 'Create Article' - Saves to database
               - 'Update Article' - Modifies database
               - 'Delete Article' - Removes from database
               - 'Publish Article' - Changes public state
               For these, call 'Ask Confirmation' tool with:
               - tool_name: "Create Article" (or whatever you intend)
               - tool_args: {{ "title": "...", "content": "..." }}
               - channel_id: "{channel_id}"
               - thread_ts: "{thread_ts}"
            
            4. **CHIT-CHAT & POLITENESS**:
               - You are a helpful, professional AI assistant.
               - If the user says "Hi", "Hello", or engages in small talk, reply politely and warmly. 
               - Briefly mention your meaningful capabilities (Creating/Managing Newsletters) to guide them back to work, but don't be robotic.
               - Example: "Hello! Hope you're having a great day. I'm ready to help you with the newsletter. Need to draft anything?"
            
            5. **FILE-BASED ARTICLE GENERATION**:
               When the user uploads a file and asks you to "write an article" or "turn this into an article":
               - IMMEDIATELY call 'Generate Content' tool with the file content as the topic/details
               - Do NOT just acknowledge - take action
               - Return the generated article text as your Final Answer
            
            6. You must return the ACTUAL GENERATED CONTENT (or confirmation message) as your Final Answer.
            """,
            expected_output="The actual generated article content with title, excerpt, and body text. Must be the output from calling the Generate Content tool, not an acknowledgment.",
            agent=selected_agent
        )
        
        result = selected_agent.execute_task(task)
        
        # Log result for debugging
        logger.info(f"Agent Result for {user_id}: {str(result)[:100]}...")
        
        # 3.5 POST-GENERATION: If we used content_generator_agent, trigger confirmation workflow
        if use_content_agent and result:
            logger.info("📋 Triggering confirmation workflow for generated content")
            
            # The agent returns formatted markdown, not JSON
            # Extract title and use the content directly
            try:
                result_str = str(result)
                
                # Extract title from markdown (first # heading)
                title_match = re.search(r'^#\s+(.+)$', result_str, re.MULTILINE)
                title = title_match.group(1) if title_match else "Generated Article"
                
                # Extract first paragraph as excerpt (non-heading text)
                lines = result_str.split('\n')
                excerpt = ""
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#') and not line.startswith('*'):
                        excerpt = line[:150]  # First 150 chars
                        break
                
                # Call the confirmation tool to create preview + buttons
                # Import the tool wrapper, then call its underlying function
                from src.tools.confirmation import ask_confirmation
                from src.tools.image import generate_image
                
                # Generate a featured image for the article
                logger.info(f"🎨 Auto-generating featured image for: {title}")
                image_result = generate_image.func(
                    description=title,
                    style="vibrant",
                    mood="inspiring",
                    aspect_ratio="16:9"
                )
                
                image_url = None
                if image_result.get("success"):
                    image_url = image_result.get("image_url")
                    logger.info(f"✅ Image generated: {image_url}")
                else:
                    logger.warning(f"⚠️ Image generation failed: {image_result.get('error')}")
                
                # Generate summary for the confirmation
                summary = f"Create article: **{title}**\n_Excerpt: {excerpt[:100] if excerpt else 'No excerpt'}..._"
                if image_url:
                    summary += f"\n🎨 _Featured image generated!_"
                
                # Call the underlying function (not the Tool wrapper)
                confirmation_result_str = ask_confirmation.func(
                    tool_name="Create Article",
                    tool_args={
                        "news_title": title,
                        "newscontent": result_str,  # Use the full markdown content
                        "news_excerpt": excerpt,
                        "news_image": image_url,  # Include generated image
                        "draft": True  # Always create as draft initially
                    },
                    summary=summary,
                    channel_id=channel_id,
                    thread_ts=thread_ts
                )
                
                logger.info(f"✅ Confirmation triggered successfully")
                
                # Update memory with the confirmation message instead
                memory.add_message(thread_ts, "assistant", confirmation_result_str)
                return  # Skip the normal say() below
                
            except Exception as e:
                logger.error(f"Error in post-generation workflow: {e}")
                import traceback
                traceback.print_exc()
                # Fall through to normal response
        
        # 3. Add Agent Response to History
        memory.add_message(thread_ts, "assistant", str(result))
        
        # Send result back to Slack
        say(str(result), thread_ts=thread_ts)
        
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        say(f"❌ I encountered an error: {str(e)}", thread_ts=thread_ts)


@app.event("message")
def handle_message(event, say):
    """Handle direct messages or messages in channels where bot is present."""
    # Ignore messages from bots
    if event.get("bot_id"):
        return

    channel_type = event.get("channel_type")
    
    # Only respond to DMs automatically, or if mentioned (handled by app_mention)
    if channel_type == "im":
        logger.info(f"Received DM from {event['user']}")
        handle_app_mention(event, say)


if __name__ == "__main__":
    if not settings.slack_app_token or settings.slack_app_token.startswith("xapp-placeholder"):
        logger.error("SLACK_APP_TOKEN not set in .env. Cannot start Socket Mode.")
    else:
        # Start Dashboard in Thread
        logger.info("🎨 Starting Dashboard on port 8000...")
        dash_thread = threading.Thread(target=start_dashboard, daemon=True)
        dash_thread.start()
        
        logger.info("⚡️ Starting Slack Bot in Socket Mode...")
        handler = SocketModeHandler(app, settings.slack_app_token)
        handler.start()
