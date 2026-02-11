"""
Temporary File Manager for Slack File Processing.
Tracks and manages cleanup of temporary files created during file processing.
"""

import logging
import os
import tempfile
from typing import List, Optional
from pathlib import Path
import atexit

logger = logging.getLogger("TempFileManager")


class TempFileManager:
    """Manages temporary files with automatic cleanup tracking."""
    
    def __init__(self):
        """Initialize temp file manager."""
        self._temp_files: List[str] = []
        # Register cleanup on program exit
        atexit.register(self.cleanup_all)
    
    def create_temp_file(self, suffix: str = "", prefix: str = "slack_") -> str:
        """
        Create a temporary file and track it for cleanup.
        
        Args:
            suffix: File suffix (e.g., ".jpg", ".png")
            prefix: File prefix
            
        Returns:
            Path to the created temporary file
        """
        tfile = tempfile.NamedTemporaryFile(
            delete=False, 
            suffix=suffix, 
            prefix=prefix
        )
        filepath = tfile.name
        tfile.close()
        
        self._temp_files.append(filepath)
        logger.info(f"📁 Created temp file: {filepath}")
        
        return filepath
    
    def write_temp_file(self, content: bytes, suffix: str = "", prefix: str = "slack_") -> str:
        """
        Create a temp file and write content to it.
        
        Args:
            content: Binary content to write
            suffix: File suffix (e.g., ".jpg", ".png")
            prefix: File prefix
            
        Returns:
            Path to the created file
        """
        filepath = self.create_temp_file(suffix=suffix, prefix=prefix)
        
        with open(filepath, 'wb') as f:
            f.write(content)
        
        logger.info(f"💾 Wrote {len(content)} bytes to {filepath}")
        return filepath
    
    def cleanup_file(self, filepath: str) -> bool:
        """
        Delete a specific temp file and remove from tracking.
        
        Args:
            filepath: Path to file to delete
            
        Returns:
            True if file was deleted, False otherwise
        """
        try:
            if os.path.exists(filepath):
                os.unlink(filepath)
                logger.info(f"🗑️  Cleaned up temp file: {filepath}")
            
            if filepath in self._temp_files:
                self._temp_files.remove(filepath)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to cleanup {filepath}: {e}")
            return False
    
    def cleanup_all(self) -> int:
        """
        Clean up all tracked temporary files.
        
        Returns:
            Number of files successfully deleted
        """
        if not self._temp_files:
            return 0
        
        logger.info(f"🧹 Cleaning up {len(self._temp_files)} temp file(s)...")
        
        cleaned = 0
        for filepath in list(self._temp_files):  # Copy list to avoid modification during iteration
            if self.cleanup_file(filepath):
                cleaned += 1
        
        logger.info(f"✅ Cleaned up {cleaned}/{len(self._temp_files)} temp files")
        return cleaned
    
    def get_tracked_files(self) -> List[str]:
        """Get list of currently tracked temp files."""
        return self._temp_files.copy()
    
    def get_tracked_count(self) -> int:
        """Get count of currently tracked temp files."""
        return len(self._temp_files)


# Global instance for the Slack bot
temp_file_manager = TempFileManager()
