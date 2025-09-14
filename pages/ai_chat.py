"""
AI Chat Page
============
Basic AI chat interface page.
"""

import streamlit as st


def render():
    """Render the AI chat page."""
    from utils.layout import render_header
    from utils.winwood_styling import apply_winwood_theme
    
    apply_winwood_theme()
    render_header("🤖 AI Chat", "Chat with AI about your business data")
    
    # Check if data is loaded
    try:
        from cloud_state_management import get_state, get_main_dataframe
        state = get_state()
        df = get_main_dataframe()
        data_loaded = state.data_loaded and df is not None
        filename = state.uploaded_filename
    except ImportError:
        # Fallback
        data_loaded = st.session_state.get('data_loaded', False)
        df = st.session_state.get('uploaded_data')
        filename = st.session_state.get('uploaded_filename', '')
    
    if not data_loaded or df is None:
        st.warning("⚠️ No data loaded. Please upload data first.")
        if st.button("← Go to Upload"):
            from controllers import go_to_stage
            go_to_stage("upload")
        return
    
    # Data info
    st.success(f"✅ Data loaded: {filename} ({df.shape[0]:,} rows × {df.shape[1]} columns)")
    
    # Simple AI chat interface
    st.subheader("💬 AI Assistant")
    st.info("This is a placeholder for the AI chat interface. In the full version, you can chat with AI about your business data, ask questions, and get insights.")
    
    # Sample chat interface
    user_question = st.text_input("Ask a question about your data:", placeholder="What insights can you find in this data?")
    
    if st.button("Send") and user_question:
        with st.chat_message("assistant"):
            st.write(f"Thank you for your question: '{user_question}'")
            st.write(f"Based on your data with {df.shape[0]} rows and {df.shape[1]} columns, here are some insights:")
            st.write("• Your data contains the following columns: " + ", ".join(df.columns.tolist()))
            if len(df) > 0:
                st.write(f"• The data has {len(df)} records")
                numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                if numeric_cols:
                    st.write(f"• Numeric columns for analysis: {', '.join(numeric_cols)}")
            st.write("\n*Note: This is a simplified response. The full AI integration provides detailed analysis and insights.*")
    
    # Navigation buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("← Upload", use_container_width=True):
            from controllers import go_to_stage
            go_to_stage("upload")
    
    with col2:
        if st.button("📊 Visualizations", use_container_width=True):
            from controllers import go_to_stage
            go_to_stage("visualizations")
    
    with col3:
        if st.button("Business Research →", use_container_width=True):
            from controllers import go_to_stage
            go_to_stage("map")