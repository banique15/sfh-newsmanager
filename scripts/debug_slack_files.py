import os
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DebugSlack")

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = "C0AAHU9J54Y"  # Extracted from user logs

def check_channel_history():
    if not SLACK_BOT_TOKEN:
        logger.error("SLACK_BOT_TOKEN not found!")
        return

    client = WebClient(token=SLACK_BOT_TOKEN)
    
    logger.info(f"Attempting to read history from channel {CHANNEL_ID}...")
    
    try:
        # Fetch last 5 messages
        result = client.conversations_history(
            channel=CHANNEL_ID,
            limit=5
        )
        
        messages = result.get("messages", [])
        logger.info(f"Successfully fetched {len(messages)} messages.")
        
        found_files = False
        for msg in messages:
            ts = msg.get("ts")
            text = msg.get("text", "")[:50]
            files = msg.get("files", [])
            
            logger.info(f"Msg {ts}: '{text}...' | Files: {len(files)}")
            
            if files:
                found_files = True
                for f in files:
                    logger.info(f"  - File: {f.get('name')} (ID: {f.get('id')}, Type: {f.get('filetype')})")
                    
        if not found_files:
            logger.warning("No files found in the last 5 messages.")
            
    except SlackApiError as e:
        logger.error(f"Slack API Error: {e.response['error']}")
        if e.response['error'] == 'missing_scope':
            logger.error(f"MISSING SCOPES: {e.response.get('needed', 'unknown')}")

if __name__ == "__main__":
    check_channel_history()
