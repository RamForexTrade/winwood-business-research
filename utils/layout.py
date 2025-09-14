"""
Layout Utilities
================
UI layout and styling utilities for the Streamlit application.
"""
import streamlit as st
from typing import Dict, Any


def setup_page_config():
    """Setup Streamlit page configuration."""
    st.set_page_config(
        page_title="Business Research Tool",
        page_icon="🏢",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def render_navigation_sidebar():
    """Render the navigation sidebar."""
    with st.sidebar:
        st.title("🏢 Business Research Tool")
        st.markdown("---")
        
        # Navigation menu
        st.subheader("Navigation")
        
        # Get current stage from session state
        try:
            from state_management import get_state
            state = get_state()
            current_stage = state.current_stage
        except:
            current_stage = "upload"
        
        # Navigation buttons
        if st.button("📤 Upload Data", use_container_width=True):
            try:
                from controllers import go_to_stage
                go_to_stage("upload")
            except:
                st.session_state.current_stage = "upload"
                st.rerun()
        
        if st.button("🔍 Web Research", use_container_width=True):
            try:
                from controllers import go_to_stage
                go_to_stage("map")
            except:
                st.session_state.current_stage = "map"
                st.rerun()
        
        if st.button("📧 Email Outreach", use_container_width=True):
            try:
                from controllers import go_to_stage
                go_to_stage("analyze")
            except:
                st.session_state.current_stage = "analyze"
                st.rerun()


def render_progress_indicator():
    """Render progress indicator."""
    try:
        from state_management import get_state
        state = get_state()
        progress = state.stage_progress
        
        st.sidebar.markdown("---")
        st.sidebar.subheader("Progress")
        
        # Progress indicators
        stages = [
            ("Upload", "upload", "📤"),
            ("Research", "map", "🔍"),
            ("Outreach", "analyze", "📧")
        ]
        
        for name, key, icon in stages:
            status = "✅" if progress.get(key, False) else "⏳"
            st.sidebar.write(f"{icon} {name}: {status}")
            
    except Exception as e:
        # Fallback if state management not available
        st.sidebar.markdown("---")
        st.sidebar.subheader("Progress")
        st.sidebar.write("📤 Upload: ⏳")
        st.sidebar.write("🔍 Research: ⏳")
        st.sidebar.write("📧 Outreach: ⏳")


def render_winwood_footer():
    """Render company footer."""
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p>🏢 <strong>Business Research Tool</strong></p>
            <p>Powered by Streamlit • Built for Business Intelligence</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_error_message(message: str, details: str = None):
    """Show formatted error message."""
    st.error(f"❌ **Error:** {message}")
    if details:
        with st.expander("Error Details"):
            st.code(details)


def show_success_message(message: str):
    """Show formatted success message."""
    st.success(f"✅ **Success:** {message}")


def show_info_message(message: str):
    """Show formatted info message."""
    st.info(f"ℹ️ **Info:** {message}")


def show_warning_message(message: str):
    """Show formatted warning message."""
    st.warning(f"⚠️ **Warning:** {message}")


def create_two_column_layout():
    """Create a two-column layout."""
    return st.columns(2)


def create_three_column_layout():
    """Create a three-column layout."""
    return st.columns(3)


def render_data_summary(df):
    """Render data summary information."""
    if df is not None and not df.empty:
        col1, col2, col3 = create_three_column_layout()
        
        with col1:
            st.metric("Rows", len(df))
        
        with col2:
            st.metric("Columns", len(df.columns))
        
        with col3:
            memory_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
            st.metric("Memory", f"{memory_mb:.1f} MB")


def render_file_upload_area():
    """Render file upload area."""
    st.subheader("📤 Upload Your Data")
    
    uploaded_file = st.file_uploader(
        "Choose a CSV or Excel file",
        type=['csv', 'xlsx', 'xls'],
        help="Upload your business data file to get started"
    )
    
    return uploaded_file


def render_loading_spinner(message: str = "Processing..."):
    """Render loading spinner with message."""
    with st.spinner(message):
        return True


def create_download_section(df, filename_prefix: str = "data"):
    """Create download section for dataframe."""
    if df is not None and not df.empty:
        st.subheader("📥 Download Data")
        
        # Convert to CSV
        csv = df.to_csv(index=False)
        
        st.download_button(
            label="📄 Download as CSV",
            data=csv,
            file_name=f"{filename_prefix}.csv",
            mime="text/csv",
            use_container_width=True
        )


def render_dataframe_preview(df, title: str = "Data Preview", max_rows: int = 5):
    """Render dataframe preview with title."""
    if df is not None and not df.empty:
        st.subheader(title)
        
        # Show basic info
        render_data_summary(df)
        
        # Show preview
        st.dataframe(df.head(max_rows), use_container_width=True)
        
        if len(df) > max_rows:
            st.caption(f"Showing first {max_rows} rows of {len(df)} total rows")


def create_filter_section():
    """Create filter section layout."""
    st.subheader("🔍 Filter Data")
    return st.container()


def create_results_section():
    """Create results section layout."""
    st.subheader("📊 Results")
    return st.container()


# Styling utilities
def apply_custom_css():
    """Apply custom CSS styling."""
    st.markdown("""
    <style>
    .main > div {
        padding-top: 2rem;
    }
    
    .stButton > button {
        width: 100%;
    }
    
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #c3e6cb;
    }
    
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #f5c6cb;
    }
    </style>
    """, unsafe_allow_html=True)


# Initialize layout
def initialize_layout():
    """Initialize the application layout."""
    setup_page_config()
    apply_custom_css()
