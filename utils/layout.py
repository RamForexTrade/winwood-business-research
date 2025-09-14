"""
Layout Utilities
===============
UI layout and styling functions.
"""

import streamlit as st
from typing import Optional


def setup_page_config():
    """Setup Streamlit page configuration."""
    st.set_page_config(
        page_title="Winwood Business Research Tool",
        page_icon="🏢",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def render_navigation_sidebar():
    """Render the navigation sidebar."""
    with st.sidebar:
        st.title("🏢 Winwood Business Research")
        st.markdown("---")
        
        # Navigation menu
        if st.button("📁 Upload Data", use_container_width=True):
            from controllers import go_to_stage
            go_to_stage("upload")
        
        if st.button("🤖 AI Chat", use_container_width=True):
            from controllers import go_to_stage
            go_to_stage("ai_chat")
        
        if st.button("📊 Visualizations", use_container_width=True):
            from controllers import go_to_stage
            go_to_stage("visualizations")
        
        if st.button("🗺️ Business Research", use_container_width=True):
            from controllers import go_to_stage
            go_to_stage("map")
        
        if st.button("📧 Email Outreach", use_container_width=True):
            from controllers import go_to_stage
            go_to_stage("analyze")
        
        st.markdown("---")
        st.markdown("**Powered by Winwood Technology**")


def render_progress_indicator():
    """Render progress indicator."""
    try:
        from controllers import get_current_stage, is_stage_complete
        
        current = get_current_stage()
        
        # Progress steps
        steps = {
            "upload": "📁 Upload",
            "ai_chat": "🤖 AI Chat", 
            "visualizations": "📊 Visualizations",
            "map": "🗺️ Research",
            "analyze": "📧 Outreach"
        }
        
        # Create progress indicator
        cols = st.columns(len(steps))
        
        for i, (stage, label) in enumerate(steps.items()):
            with cols[i]:
                if stage == current:
                    st.markdown(f"**{label}** ⭐")
                elif is_stage_complete(stage):
                    st.markdown(f"{label} ✅")
                else:
                    st.markdown(f"{label}")
        
        st.markdown("---")
    
    except Exception as e:
        st.error(f"Error rendering progress: {e}")


def render_header(title: str, subtitle: Optional[str] = None):
    """Render page header."""
    st.title(title)
    if subtitle:
        st.markdown(subtitle)
    st.markdown("---")