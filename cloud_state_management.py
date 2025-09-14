"""
Cloud State Management Module
============================
Cloud-optimized state management for Railway deployment.
Uses in-memory storage with minimal disk usage.
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
import streamlit as st
import pandas as pd
import uuid
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CloudAppState:
    """Cloud-optimized application state using dataclass."""
    
    # Session Management - Cloud Optimized
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_created: str = field(default_factory=lambda: datetime.now().isoformat())
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())
    cloud_mode: bool = True  # Flag for cloud deployment
    
    # Navigation state
    current_stage: str = "upload"
    
    # Stage Progress Tracking
    stage_progress: Dict[str, bool] = field(default_factory=lambda: {
        'upload': False,
        'map': False, 
        'analyze': False
    })
    
    # Data state - References only (actual data in cloud session manager)
    uploaded_filename: str = ""
    data_loaded: bool = False
    data_size_mb: float = 0.0
    data_rows: int = 0
    data_columns: int = 0
    
    # Filter state
    filters_applied: Dict[str, Any] = field(default_factory=dict)
    primary_filter_column: str = ""
    primary_filter_values: list = field(default_factory=list)
    secondary_filter_column: str = ""
    secondary_filter_values: list = field(default_factory=list)
    
    # Analysis state
    analysis_complete: bool = False
    results_generated: bool = False
    
    # Email state
    email_config: Dict[str, Any] = field(default_factory=dict)
    emails_sent: int = 0
    
    # UI state
    show_debug: bool = False
    
    # Cloud-specific settings
    memory_limit_mb: float = 100.0  # Memory limit for this session
    auto_cleanup: bool = True


# Global state key
CLOUD_STATE_KEY = "cloud_app_state"


def initialize_cloud_state() -> None:
    """Initialize cloud-optimized application state."""
    try:
        if CLOUD_STATE_KEY not in st.session_state:
            # Create new cloud state
            state = CloudAppState()
            st.session_state[CLOUD_STATE_KEY] = state
            logger.info(f"Initialized cloud state with session: {state.session_id}")
        else:
            # Update timestamp for existing state
            state = st.session_state[CLOUD_STATE_KEY]
            state.last_updated = datetime.now().isoformat()
    except Exception as e:
        logger.error(f"Error initializing cloud state: {e}")
        # Fallback: Create minimal state
        st.session_state[CLOUD_STATE_KEY] = CloudAppState()


def get_cloud_state() -> CloudAppState:
    """Get current cloud application state."""
    if CLOUD_STATE_KEY not in st.session_state:
        initialize_cloud_state()
    
    return st.session_state[CLOUD_STATE_KEY]


def update_cloud_state(**kwargs) -> None:
    """Update cloud application state with new values."""
    try:
        state = get_cloud_state()
        
        # Update state attributes
        for key, value in kwargs.items():
            if hasattr(state, key):
                setattr(state, key, value)
            else:
                logger.warning(f"Attempted to set unknown state attribute: {key}")
        
        # Update timestamp
        state.last_updated = datetime.now().isoformat()
        
    except Exception as e:
        logger.error(f"Error updating cloud state: {e}")


def store_dataframe_in_cloud(df: pd.DataFrame, name: str = "main_data") -> bool:
    """Store dataframe using simple session state."""
    try:
        # Simple storage in session state for Railway deployment
        st.session_state[f'dataframe_{name}'] = df
        
        # Update state metadata
        size_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
        update_cloud_state(
            data_loaded=True,
            data_size_mb=round(size_mb, 2),
            data_rows=len(df),
            data_columns=len(df.columns)
        )
        logger.info(f"Stored dataframe '{name}' ({size_mb:.1f}MB) in session state")
        return True
        
    except Exception as e:
        logger.error(f"Error storing dataframe: {e}")
        return False


def load_dataframe_from_cloud(name: str = "main_data") -> Optional[pd.DataFrame]:
    """Load dataframe from simple session state."""
    try:
        return st.session_state.get(f'dataframe_{name}')
    except Exception as e:
        logger.error(f"Error loading dataframe: {e}")
        return None


def get_main_dataframe() -> Optional[pd.DataFrame]:
    """Get the main dataframe from storage."""
    return load_dataframe_from_cloud("main_data")


def set_main_dataframe(df: pd.DataFrame) -> bool:
    """Set the main dataframe in storage."""
    return store_dataframe_in_cloud(df, "main_data")


def get_filtered_dataframe() -> Optional[pd.DataFrame]:
    """Get the filtered dataframe from storage."""
    return load_dataframe_from_cloud("filtered_data")


def set_filtered_dataframe(df: pd.DataFrame) -> bool:
    """Set the filtered dataframe in storage."""
    return store_dataframe_in_cloud(df, "filtered_data")


# Backward compatibility functions
def initialize_state() -> None:
    """Backward compatibility wrapper."""
    initialize_cloud_state()


def get_state() -> CloudAppState:
    """Backward compatibility wrapper."""
    return get_cloud_state()


def update_state(**kwargs) -> None:
    """Backward compatibility wrapper."""
    update_cloud_state(**kwargs)


# Simplified version for Railway deployment without heavy dependencies
class SimpleState:
    """Simplified state management for basic deployment."""
    
    def __init__(self):
        self.current_stage = "upload"
        self.data_loaded = False
        self.uploaded_filename = ""
        self.cloud_mode = True
        
    def to_dict(self):
        return {
            'current_stage': self.current_stage,
            'data_loaded': self.data_loaded,
            'uploaded_filename': self.uploaded_filename,
            'cloud_mode': self.cloud_mode
        }


# Fallback simple state management
def get_simple_state():
    """Get simple state for minimal deployment."""
    if 'simple_state' not in st.session_state:
        st.session_state.simple_state = SimpleState()
    return st.session_state.simple_state