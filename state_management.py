"""
Local State Management (Fallback)
================================
Fallback state management for local development.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import streamlit as st
import pandas as pd
import uuid
from datetime import datetime


@dataclass
class AppState:
    """Application state for local development."""
    
    # Session Management
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    current_stage: str = "upload"
    
    # Data state
    uploaded_filename: str = ""
    data_loaded: bool = False
    
    # Progress tracking
    stage_progress: Dict[str, bool] = field(default_factory=lambda: {
        'upload': False,
        'map': False,
        'analyze': False
    })


STATE_KEY = "app_state"


def initialize_state() -> None:
    """Initialize application state."""
    if STATE_KEY not in st.session_state:
        st.session_state[STATE_KEY] = AppState()


def get_state() -> AppState:
    """Get current application state."""
    if STATE_KEY not in st.session_state:
        initialize_state()
    return st.session_state[STATE_KEY]


def update_state(**kwargs) -> None:
    """Update application state."""
    state = get_state()
    for key, value in kwargs.items():
        if hasattr(state, key):
            setattr(state, key, value)