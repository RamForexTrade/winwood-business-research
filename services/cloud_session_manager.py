"""
Simplified Cloud Session Manager for Railway Deployment
======================================================
Basic in-memory session management for cloud deployment.
"""

import streamlit as st
import pandas as pd
import os
import logging
from typing import Optional, Dict, Any
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CloudSessionManager:
    """Simplified cloud session manager for Railway deployment."""
    
    def __init__(self):
        # Use in-memory storage only
        if 'cloud_sessions' not in st.session_state:
            st.session_state.cloud_sessions = {}
        
        logger.info("Cloud Session Manager initialized")
    
    def create_session(self, session_id: str) -> str:
        """Create a new session."""
        st.session_state.cloud_sessions[session_id] = {
            'created_at': st.session_state.get('session_start_time', 'unknown'),
            'data': {},
            'metadata': {}
        }
        logger.info(f"Created session: {session_id}")
        return session_id
    
    def store_dataframe(self, session_id: str, df: pd.DataFrame, name: str) -> bool:
        """Store dataframe in session."""
        try:
            if session_id not in st.session_state.cloud_sessions:
                self.create_session(session_id)
            
            # Store in session state
            st.session_state.cloud_sessions[session_id]['data'][name] = df
            logger.info(f"Stored dataframe '{name}' in session {session_id}")
            return True
        except Exception as e:
            logger.error(f"Error storing dataframe: {e}")
            return False
    
    def load_dataframe(self, session_id: str, name: str) -> Optional[pd.DataFrame]:
        """Load dataframe from session."""
        try:
            if session_id in st.session_state.cloud_sessions:
                return st.session_state.cloud_sessions[session_id]['data'].get(name)
            return None
        except Exception as e:
            logger.error(f"Error loading dataframe: {e}")
            return None
    
    def store_session_metadata(self, session_id: str, metadata: Dict[str, Any]) -> bool:
        """Store session metadata."""
        try:
            if session_id not in st.session_state.cloud_sessions:
                self.create_session(session_id)
            
            st.session_state.cloud_sessions[session_id]['metadata'] = metadata
            return True
        except Exception as e:
            logger.error(f"Error storing metadata: {e}")
            return False
    
    def create_export_file(self, session_id: str, df: pd.DataFrame, filename: str):
        """Create export file buffer."""
        try:
            buffer = BytesIO()
            if filename.endswith('.csv'):
                df.to_csv(buffer, index=False)
            elif filename.endswith('.xlsx'):
                df.to_excel(buffer, index=False)
            buffer.seek(0)
            return buffer
        except Exception as e:
            logger.error(f"Error creating export file: {e}")
            return None
    
    def cleanup_session(self, session_id: str) -> bool:
        """Cleanup session data."""
        try:
            if session_id in st.session_state.cloud_sessions:
                del st.session_state.cloud_sessions[session_id]
            return True
        except Exception as e:
            logger.error(f"Error cleaning up session: {e}")
            return False
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get session statistics."""
        return {
            'active_sessions': len(st.session_state.get('cloud_sessions', {})),
            'total_data_objects': sum(len(session.get('data', {})) for session in st.session_state.get('cloud_sessions', {}).values())
        }
    
    def force_cleanup_all(self) -> None:
        """Force cleanup all sessions."""
        st.session_state.cloud_sessions = {}
        logger.info("All sessions cleaned up")


# Global instance
_cloud_session_manager = None


def get_cloud_session_manager() -> CloudSessionManager:
    """Get global cloud session manager instance."""
    global _cloud_session_manager
    if _cloud_session_manager is None:
        _cloud_session_manager = CloudSessionManager()
    return _cloud_session_manager