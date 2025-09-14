"""
Quick Visualizations Page
=========================
Basic data visualization page.
"""

import streamlit as st
import pandas as pd
import plotly.express as px


def render():
    """Render the visualizations page."""
    from utils.layout import render_header
    from utils.winwood_styling import apply_winwood_theme
    
    apply_winwood_theme()
    render_header("📊 Quick Visualizations", "Explore your data with interactive charts")
    
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
    
    st.success(f"✅ Data loaded: {filename} ({df.shape[0]:,} rows × {df.shape[1]} columns)")
    
    # Basic visualizations
    st.subheader("📈 Data Overview")
    
    # Data summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Rows", f"{len(df):,}")
        st.metric("Total Columns", len(df.columns))
    
    with col2:
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        text_cols = df.select_dtypes(include=['object']).columns.tolist()
        st.metric("Numeric Columns", len(numeric_cols))
        st.metric("Text Columns", len(text_cols))
    
    # Simple visualizations
    if len(numeric_cols) > 0:
        st.subheader("📊 Numeric Data Visualizations")
        
        # Select columns for visualization
        if len(numeric_cols) >= 1:
            selected_col = st.selectbox("Select a numeric column to visualize:", numeric_cols)
            
            if selected_col:
                # Histogram
                fig_hist = px.histogram(df, x=selected_col, title=f"Distribution of {selected_col}")
                st.plotly_chart(fig_hist, use_container_width=True)
        
        if len(numeric_cols) >= 2:
            st.subheader("🔄 Correlation Analysis")
            col1_corr = st.selectbox("Select first column:", numeric_cols, key="corr1")
            col2_corr = st.selectbox("Select second column:", numeric_cols, key="corr2")
            
            if col1_corr != col2_corr:
                fig_scatter = px.scatter(df, x=col1_corr, y=col2_corr, title=f"{col1_corr} vs {col2_corr}")
                st.plotly_chart(fig_scatter, use_container_width=True)
    
    if len(text_cols) > 0:
        st.subheader("📝 Text Data Analysis")
        
        selected_text_col = st.selectbox("Select a text column to analyze:", text_cols)
        
        if selected_text_col:
            # Value counts
            value_counts = df[selected_text_col].value_counts().head(10)
            
            if len(value_counts) > 0:
                fig_bar = px.bar(
                    x=value_counts.values, 
                    y=value_counts.index, 
                    orientation='h',
                    title=f"Top 10 values in {selected_text_col}"
                )
                fig_bar.update_layout(yaxis_title=selected_text_col, xaxis_title="Count")
                st.plotly_chart(fig_bar, use_container_width=True)
    
    # Data table
    st.subheader("📋 Raw Data")
    st.dataframe(df, use_container_width=True)
    
    # Navigation
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("← AI Chat", use_container_width=True):
            from controllers import go_to_stage
            go_to_stage("ai_chat")
    
    with col2:
        if st.button("🗺️ Business Research", use_container_width=True):
            from controllers import go_to_stage
            go_to_stage("map")
    
    with col3:
        if st.button("Email Outreach →", use_container_width=True):
            from controllers import go_to_stage
            go_to_stage("analyze")