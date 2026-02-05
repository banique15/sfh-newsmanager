"""
Context Memory Manager for Slack Bot.
Stores conversation history to allow multi-turn interactions.
Currently uses a simple JSON file for persistence.
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Any

# File to store history
HISTORY_FILE = "conversation_history.json"
MAX_HISTORY_PER_THREAD = 10

logger = logging.getLogger(__name__)

class ContextMemory:
    def __init__(self, file_path: str = HISTORY_FILE):
        self.file_path = file_path
        self.history: Dict[str, List[Dict[str, Any]]] = {}
        self._load_memory()

    def _load_memory(self):
        """Load history from file."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.history = data
            except Exception as e:
                logger.error(f"Failed to load memory: {e}")
                self.history = {}

    def _save_memory(self):
        """Save history to file."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save memory: {e}")

    def add_message(self, thread_id: str, role: str, content: str):
        """
        Add a message to the thread history.
        role: 'user' or 'assistant'
        """
        if thread_id not in self.history:
            self.history[thread_id] = []
        
        # Add message
        self.history[thread_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Trim history
        if len(self.history[thread_id]) > MAX_HISTORY_PER_THREAD:
            self.history[thread_id] = self.history[thread_id][-MAX_HISTORY_PER_THREAD:]
            
        self._save_memory()

    def get_history(self, thread_id: str) -> List[Dict[str, Any]]:
        """Get history for a thread."""
        return self.history.get(thread_id, [])

    def get_formatted_history(self, thread_id: str) -> str:
        """Get history formatted as a string for LLM context."""
        history = self.get_history(thread_id)
        if not history:
            return ""
            
        formatted = "PREVIOUS CONVERSATION HISTORY:\n"
        for msg in history:
            role = "User" if msg["role"] == "user" else "Assistant"
            formatted += f"{role}: {msg['content']}\n"
        
        formatted += "\n(Use this history to understand context, referrals to 'it' or 'that', and previous actions)\n"
        return formatted

    def clear_history(self, thread_id: str):
        """Clear history for a thread."""
        if thread_id in self.history:
            del self.history[thread_id]
            self._save_memory()


# Global memory instance
memory = ContextMemory()
