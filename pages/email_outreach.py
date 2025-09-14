"""
Email Outreach Page
==================
Email campaign management and outreach functionality.
"""

import streamlit as st
import pandas as pd


def render():
    """Render the email outreach page."""
    from utils.layout import render_header
    from utils.winwood_styling import apply_winwood_theme
    
    apply_winwood_theme()
    render_header("📧 Email Outreach", "Manage email campaigns and outreach")
    
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
    
    # Email outreach interface
    st.subheader("📬 Email Campaign Setup")
    
    # Campaign configuration
    campaign_name = st.text_input("Campaign Name:", placeholder="Q1 Business Outreach Campaign")
    
    # Email template
    st.subheader("📝 Email Template")
    
    email_subject = st.text_input(
        "Email Subject:", 
        placeholder="Business Partnership Opportunity"
    )
    
    email_template = st.text_area(
        "Email Template:",
        placeholder="Dear [Company Name],\n\nWe hope this email finds you well...\n\nBest regards,\n[Your Name]",
        height=200
    )
    
    # Target selection
    st.subheader("🎯 Target Selection")
    
    # Find email columns
    email_cols = [col for col in df.columns if any(keyword in col.lower() for keyword in ['email', 'mail', 'contact'])]
    
    if email_cols:
        selected_email_col = st.selectbox("Select email column:", email_cols)
        
        if selected_email_col:
            # Show email data
            email_data = df[selected_email_col].dropna()
            st.info(f"Found {len(email_data)} email addresses in {selected_email_col}")
            
            # Preview targets
            if len(email_data) > 0:
                st.subheader("📋 Target Preview")
                target_preview = df[[col for col in df.columns if col in ['Company', 'Name', selected_email_col] or 'company' in col.lower() or 'name' in col.lower()]]
                st.dataframe(target_preview.head(10), use_container_width=True)
    else:
        st.warning("No email columns found in the data. Please ensure your data includes email addresses.")
    
    # Campaign actions
    st.subheader("🚀 Campaign Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Preview Campaign", use_container_width=True):
            if campaign_name and email_subject and email_template:
                st.success("Campaign preview generated!")
                with st.expander("Campaign Preview"):
                    st.write(f"**Campaign:** {campaign_name}")
                    st.write(f"**Subject:** {email_subject}")
                    st.write(f"**Template:**")
                    st.code(email_template)
                    if email_cols:
                        st.write(f"**Targets:** {len(df)} potential recipients")
            else:
                st.error("Please fill in all campaign details")
    
    with col2:
        if st.button("📧 Send Test Email", use_container_width=True):
            st.info("Test email functionality would send a sample email here")
    
    with col3:
        if st.button("🚀 Launch Campaign", use_container_width=True):
            st.info("Campaign launch functionality would begin sending emails here")
            st.warning("Note: This is a demo version. No actual emails will be sent.")
    
    # Campaign analytics placeholder
    st.subheader("📈 Campaign Analytics")
    
    # Mock analytics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Emails Sent", "0")
    
    with col2:
        st.metric("Open Rate", "0%")
    
    with col3:
        st.metric("Click Rate", "0%")
    
    with col4:
        st.metric("Response Rate", "0%")
    
    st.info("📈 Campaign analytics will be displayed here after launching campaigns")
    
    # Navigation
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("← Business Research", use_container_width=True):
            from controllers import go_to_stage
            go_to_stage("map")
    
    with col2:
        if st.button("📊 Visualizations", use_container_width=True):
            from controllers import go_to_stage
            go_to_stage("visualizations")
    
    with col3:
        if st.button("📁 Upload New Data", use_container_width=True):
            from controllers import go_to_stage
            go_to_stage("upload")