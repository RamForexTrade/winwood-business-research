"""
Business Research Tool
=====================
Main application entry point for the Streamlit business research tool.
Auto-detects cloud deployment and optimizes accordingly.
"""
import streamlit as st
import os
import logging

# Health check for cloud deployment
if st.query_params.get("health") == "check":
    from health_check import *

# Auto-detect cloud deployment
is_cloud = any(env_var in os.environ for env_var in ['RAILWAY_ENVIRONMENT', 'RAILWAY_PROJECT_ID'])

# Import appropriate modules based on deployment
if is_cloud:
    from cloud_state_management import initialize_state, get_state
    from railway_config import get_railway_config
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Running in cloud mode - using optimized session management")
else:
    from state_management import initialize_state, get_state

from utils.layout import setup_page_config, render_navigation_sidebar, render_progress_indicator


def main():
    """Main application entry point."""
    # Setup
    setup_page_config()
    initialize_state()
    
    # Get current state
    state = get_state()
    
    # Render layout
    render_navigation_sidebar()
    render_progress_indicator()
    
    # Route to appropriate page based on state
    if state.current_stage == "upload":
        from pages.upload import render
        render()
    
    elif state.current_stage == "ai_chat":
        from pages.ai_chat import render
        render()
    
    elif state.current_stage == "visualizations":
        from pages.quick_visualizations import render
        render()
    
    elif state.current_stage == "map":
        # Use the business research page
        try:
            from pages.business_research import enhanced_business_research_page
            enhanced_business_research_page()
        except Exception as e:
            st.error(f"Error loading business research page: {str(e)}")
            st.error("Please try refreshing the page or contact support if the issue persists.")
            
            # Reset to upload stage as fallback
            if st.button("🔄 Return to Upload"):
                from controllers import go_to_stage
                go_to_stage("upload")
    
    elif state.current_stage == "analyze":
        from pages.email_outreach import render
        render()
    
    else:
        st.error(f"Unknown stage: {state.current_stage}")
        if st.button("Go to Upload"):
            from controllers import go_to_stage
            go_to_stage("upload")
    
    # Add company footer
    from utils.winwood_styling import render_winwood_footer
    render_winwood_footer()


if __name__ == "__main__":
    main()
