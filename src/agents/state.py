import json
import logging
import os
from typing import Any, Dict, Optional
from datetime import datetime

# Configure logging
logger = logging.getLogger("StateManager")

class StateManager:
    """
    Manages persistent state for the agent, specifically 'Pending Actions'.
    Using a JSON file ensures state survives bot restarts.
    """
    
    def __init__(self, storage_file: str = "pending_actions.json"):
        self.storage_file = storage_file
        self._state: Dict[str, Any] = {}
        self._load_state()

    def _load_state(self):
        """Load state from JSON file."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    self._state = json.load(f)
            except json.JSONDecodeError:
                logger.error(f"Corrupt state file {self.storage_file}. Starting fresh.")
                self._state = {}
            except Exception as e:
                logger.error(f"Error loading state: {e}")
                self._state = {}
        else:
            self._state = {}

    def _save_state(self):
        """Save state to JSON file."""
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(self._state, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving state: {e}")

    def set_pending_action(self, thread_ts: str, action_data: Dict[str, Any]):
        """
        Store a pending action for a specific thread.
        
        Args:
            thread_ts: The Slack thread timestamp (unique conversation ID).
            action_data: Dictionary containing tool_name, tool_args, summary, etc.
        """
        self._state[thread_ts] = {
            "data": action_data,
            "timestamp": datetime.now().isoformat()
        }
        self._save_state()
        logger.info(f"Pending action saved for thread {thread_ts}")

    def get_pending_action(self, thread_ts: str) -> Optional[Dict[str, Any]]:
        """Retrieve the pending action for a thread, if any."""
        entry = self._state.get(thread_ts)
        if entry:
            return entry.get("data")
        return None

    def clear_pending_action(self, thread_ts: str):
        """Remove the pending action for a thread (after execution or denial)."""
        if thread_ts in self._state:
            del self._state[thread_ts]
            self._save_state()
            logger.info(f"Pending action cleared for thread {thread_ts}")

# Global instance
state_manager = StateManager()
