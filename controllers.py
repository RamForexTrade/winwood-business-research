"""
Application Controllers
======================
Main navigation and stage control functions.
"""

import streamlit as st
from typing import Optional


def go_to_stage(stage: str) -> None:
    """Navigate to a specific stage."""
    # Import state management based on deployment
    try:
        from cloud_state_management import get_state, update_state
        state = get_state()
        update_state(current_stage=stage)
    except ImportError:
        # Fallback to simple state
        if 'current_stage' not in st.session_state:
            st.session_state.current_stage = 'upload'
        st.session_state.current_stage = stage
    
    st.rerun()


def get_current_stage() -> str:
    """Get current application stage."""
    try:
        from cloud_state_management import get_state
        return get_state().current_stage
    except ImportError:
        return st.session_state.get('current_stage', 'upload')


def mark_stage_complete(stage: str) -> None:
    """Mark a stage as complete."""
    try:
        from cloud_state_management import get_state, update_state
        state = get_state()
        progress = state.stage_progress.copy()
        progress[stage] = True
        update_state(stage_progress=progress)
    except ImportError:
        # Fallback
        if 'stage_progress' not in st.session_state:
            st.session_state.stage_progress = {}
        st.session_state.stage_progress[stage] = True


def is_stage_complete(stage: str) -> bool:
    """Check if a stage is complete."""
    try:
        from cloud_state_management import get_state
        return get_state().stage_progress.get(stage, False)
    except ImportError:
        progress = st.session_state.get('stage_progress', {})
        return progress.get(stage, False)