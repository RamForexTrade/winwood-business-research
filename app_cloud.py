"""
Business Research Tool - Cloud Optimized
=========================================
Main application entry point for Railway deployment.
Optimized for cloud environments with in-memory session management.
"""
import streamlit as st
import os
import logging
from railway_config import get_railway_config, is_cloud_deployment

# Configure logging for cloud deployment
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import appropriate state management based on deployment
if is_cloud_deployment():
    from cloud_state_management import initialize_state, get_state
    logger.info("Running in cloud mode - using in-memory session management")
else:
    from state_management import initialize_state, get_state
    logger.info("Running in local mode - using disk-based session management")

from utils.layout import setup_page_config, render_navigation_sidebar, render_progress_indicator


def main():
    """Main application entry point - Cloud optimized."""
    try:
        # Setup page config
        setup_page_config()
        
        # Get configuration
        railway_config = get_railway_config()
        config = railway_config.get_config()
        
        # Initialize state management
        initialize_state()
        
        # Get current state
        state = get_state()
        
        # Cloud deployment info (in debug mode only)
        if config.get('enable_debug') and state.show_debug:
            with st.sidebar.expander("🚀 Cloud Info", expanded=False):
                st.write(f"**Environment:** {config['environment']}")
                st.write(f"**Storage:** {config['storage_strategy']}")
                st.write(f"**Memory Limit:** {config['memory_limit_mb']}MB")
                st.write(f"**Max Sessions:** {config['max_sessions']}")
                
                if is_cloud_deployment():
                    from cloud_state_management import get_cloud_session_stats
                    stats = get_cloud_session_stats()
                    st.json(stats)
        
        # Render layout
        render_navigation_sidebar()
        render_progress_indicator()
        
        # Add cloud-specific warnings if needed
        if is_cloud_deployment() and state.data_size_mb > config['max_file_size_mb']:
            st.warning(f"⚠️ Large dataset ({state.data_size_mb:.1f}MB) detected. "
                      f"Cloud deployment limit is {config['max_file_size_mb']}MB. "
                      f"Consider filtering your data first.")
        
        # Route to appropriate page based on state
        if state.current_stage == "upload":
            from pages.upload import render
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
    
    except Exception as e:
        # Enhanced error handling for cloud deployment
        logger.error(f"Application error: {str(e)}")
        
        st.error("🚨 Application Error")
        st.error(f"An unexpected error occurred: {str(e)}")
        
        # In cloud deployment, offer recovery options
        if is_cloud_deployment():
            st.info("🔧 **Recovery Options:**")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔄 Restart Session"):
                    if 'cloud_state_management' in globals():
                        from cloud_state_management import cleanup_cloud_session
                        cleanup_cloud_session()
                    st.rerun()
            
            with col2:
                if st.button("🧹 Clear All Data"):
                    if 'cloud_state_management' in globals():
                        from cloud_state_management import force_cleanup_all_sessions
                        force_cleanup_all_sessions()
                    st.rerun()
            
            st.warning("If the problem persists, try refreshing your browser.")
        else:
            st.info("Please refresh the page or restart the application.")


if __name__ == "__main__":
    main()
