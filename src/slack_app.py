"""
Slack Application Entry Point.
Runs the Slack Bot in Socket Mode using Slack Bolt sdk.
"""

import logging
import os
import re

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError

from src.agents import newsletter_agent
from src.config.settings import settings
from src.agents.memory import memory
from crewai import Task

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SlackBot")

# Initialize Bolt App
app = App(
    token=settings.slack_bot_token,
    signing_secret=settings.slack_signing_secret
)

@app.event("app_mention")
def handle_app_mention(event, say):
    """Handle when bot is mentioned (@Newsletter Manager)."""
    channel_id = event["channel"]
    user_id = event["user"]
    text = event["text"]
    thread_ts = event.get("thread_ts", event["ts"])
    
    # Clean text (remove mention)
    text = re.sub(r"<@\w+>", "", text).strip()
    
    if not text:
        say("Hello! I'm the Newsletter Manager. How can I help you? try 'help'", thread_ts=thread_ts)
        return

    logger.info(f"Received mention in {channel_id}: {text}")
    
    # 1. Add User Message to History
    memory.add_message(thread_ts, "user", text)
    
    # 2. Get Context
    history_context = memory.get_formatted_history(thread_ts)
    
    # Notify user we are working on it
    # reaction = app.client.reactions_add(name="thinking_face", channel=channel_id, timestamp=event["ts"])
    say(f"👋 Hi <@{user_id}>, I'm looking into that...", thread_ts=thread_ts)
    
    # Run Agent
    try:
        task = Task(
            description=f"""User request from Slack channel {channel_id}: {text}
            
            {history_context}
            
            DIRECTIVE:
            You are an autonomous agent. When asked to generate content, you MUST call the tool 'Generate Content'.
            IDLE CHIT-CHAT IS FORBIDDEN for this task.
            
            You must return the ACTUAL GENERATED CONTENT from the tool call as your Final Answer.
            Do not say "I have generated it". Show it.
            """,
            expected_output="The full text of the article or the image URL.",
            agent=newsletter_agent
        )
        
        result = newsletter_agent.execute_task(task)
        
        # Log result for debugging
        logger.info(f"Agent Result for {user_id}: {str(result)[:100]}...")
        
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
    text = event.get("text", "")
    
    # Only respond to DMs automatically, or if mentioned (handled by app_mention)
    if channel_type == "im":
        logger.info(f"Received DM from {event['user']}: {text}")
        handle_app_mention(event, say)


@app.action("approve_action")
def handle_approve(ack, body, say):
    """Handle approve button click."""
    ack()
    user_id = body["user"]["id"]
    say(f"✅ Request approved by <@{user_id}>! Proceeding...", thread_ts=body["container"]["message_ts"])
    # In a real scenario, this would trigger a resume of the agent state or a new task
    # For now, we acknowledge.


@app.action("deny_action")
def handle_deny(ack, body, say):
    """Handle deny button click."""
    ack()
    user_id = body["user"]["id"]
    say(f"❌ Request denied by <@{user_id}>. Action cancelled.", thread_ts=body["container"]["message_ts"])


if __name__ == "__main__":
    if not settings.slack_app_token or settings.slack_app_token.startswith("xapp-placeholder"):
        logger.error("SLACK_APP_TOKEN not set in .env. Cannot start Socket Mode.")
    else:
        logger.info("⚡️ Starting Slack Bot in Socket Mode...")
        handler = SocketModeHandler(app, settings.slack_app_token)
        handler.start()
