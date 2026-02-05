"""Slack tools for CrewAI."""

import json
from typing import Any, Dict, List, Optional

from crewai.tools import tool
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from src.config.settings import settings


def get_slack_client() -> WebClient | None:
    """Get Slack WebClient if token is configured."""
    if not settings.slack_bot_token or settings.slack_bot_token.startswith("xoxb-placeholder"):
        return None
    return WebClient(token=settings.slack_bot_token)


@tool("Slack Bot")
def slack_tool(
    action: str,
    channel_id: Optional[str] = None,
    message: Optional[str] = None,
    blocks: Optional[List[Dict[str, Any]]] = None,
    thread_ts: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Interact with Slack to send messages and confirmations.
    
    Args:
        action: 'send_message' or 'send_confirmation'
        channel_id: Channel ID to send to (required for sending)
        message: Text message to send
        blocks: Optional Block Kit blocks for rich formatting
        thread_ts: Optional thread timestamp to reply in thread
        
    Returns:
        Dictionary with result of the operation
    """
    client = get_slack_client()
    if not client:
        return {
            "success": False,
            "error": "Slack not configured. Please set SLACK_BOT_TOKEN in .env.",
        }

    try:
        if action == "send_message":
            if not channel_id:
                return {"success": False, "error": "channel_id is required for send_message"}
            
            response = client.chat_postMessage(
                channel=channel_id,
                text=message or "New message",
                blocks=blocks,
                thread_ts=thread_ts
            )
            return {
                "success": True,
                "ts": response["ts"],
                "channel": response["channel"],
                "message": f"Message sent to {channel_id}"
            }
            
        elif action == "send_confirmation":
            if not channel_id or not message:
                return {"success": False, "error": "channel_id and message required for confirmation"}
                
            # Create interactive buttons
            confirm_blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": message
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
                                "text": "❌ Deny",
                                "emoji": True
                            },
                            "style": "danger",
                            "value": "deny",
                            "action_id": "deny_action"
                        }
                    ]
                }
            ]
            
            response = client.chat_postMessage(
                channel=channel_id,
                text=message, # Fallback text
                blocks=confirm_blocks,
                thread_ts=thread_ts
            )
            return {
                "success": True,
                "ts": response["ts"],
                "channel": response["channel"],
                "message": "Confirmation sent"
            }
            
        else:
            return {"success": False, "error": f"Unknown action: {action}"}

    except SlackApiError as e:
        return {
            "success": False,
            "error": f"Slack API Error: {e.response['error']}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


__all__ = ["slack_tool"]
