from typing import Any, Dict, Optional
import json
from crewai.tools import tool
from src.tools.slack import get_slack_client
from src.agents.state import state_manager

@tool("Ask Confirmation")
def ask_confirmation(
    tool_name: str,
    tool_args: Dict[str, Any],
    summary: str,
    channel_id: str,
    thread_ts: str
) -> str:
    """
    Ask for user confirmation before performing a regular action.
    ALWAYS use this instead of calling 'Create Article', 'Update Article', 'Delete Article', or 'Publish Article' directly.
    
    Args:
        tool_name: The name of the tool you would like to execute (e.g., 'Create Article').
        tool_args: The arguments you would pass to that tool (as a dictionary).
        summary: A human-readable summary of what you are about to do.
        channel_id: The Slack channel ID where the request came from.
        thread_ts: The thread timestamp of the conversation.
        
    Returns:
        A message indicating that confirmation has been requested.
    """
    # 1. Save state
    pending_data = {
        "tool_name": tool_name.replace(" ", "_").lower(), # Normalize to snake_case if agent passes "Create Article"
        "tool_args": tool_args,
        "summary": summary
    }
    
    # Mapping friendly names to actual function names if needed
    # (The agent might say "Create Article" but the function is "create_article")
    # For now, we assume the agent sends roughly the right name, or we normalize.
    # We will handle the mapping in slack_app.py Execution phase.
    
    state_manager.set_pending_action(thread_ts, pending_data)
    
    # 2. Prepare Slack Message with Buttons
    client = get_slack_client()
    if not client:
        return "Error: Slack not configured."

    preview_url = f"http://localhost:8000/preview/pending/{thread_ts}"
    
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"🛑 *Approval Needed*\n{summary}"
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "✅ Approve",
                        "emoji": True
                    },
                    "style": "primary",
                    "value": "approve",
                    "action_id": "approve_action"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "👀 View Preview",
                        "emoji": True
                    },
                    "url": preview_url,
                    "action_id": "preview_action"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "❌ Deny",
                        "emoji": True
                    },
                    "style": "danger",
                    "value": "deny",
                    "action_id": "deny_action"
                }
            ]
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "Click 'View Preview' to see the draft formatted on the web."
                }
            ]
        }
    ]

    try:
        client.chat_postMessage(
            channel=channel_id,
            text=f"Approval Needed: {summary}",
            blocks=blocks,
            thread_ts=thread_ts
        )
        return "✅ Confirmation request sent to Slack. I am now waiting for the user to click Approve or Deny. I will stop here."
    except Exception as e:
        return f"Error sending confirmation: {str(e)}"
