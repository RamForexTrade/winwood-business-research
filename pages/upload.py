"""
Upload Page
===========
Data upload and initial processing page.
"""

import streamlit as st
import pandas as pd
from typing import Optional


def render():
    """Render the upload page."""
    from utils.layout import render_header
    from utils.winwood_styling import apply_winwood_theme
    
    apply_winwood_theme()
    render_header("📁 Data Upload", "Upload your business data to get started")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a CSV or Excel file",
        type=['csv', 'xlsx', 'xls'],
        help="Upload your business data file to begin analysis"
    )
    
    if uploaded_file is not None:
        try:
            # Load data
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Display basic info
            st.success(f"✅ Successfully loaded {uploaded_file.name}")
            st.info(f"📊 Data Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
            
            # Preview data
            st.subheader("📋 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Column info
            st.subheader("📈 Column Information")
            col_info = pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes,
                'Non-Null Count': df.count(),
                'Null Count': df.isnull().sum()
            })
            st.dataframe(col_info, use_container_width=True)
            
            # Store data and proceed
            if st.button("✅ Confirm Upload & Continue", type="primary", use_container_width=True):
                try:
                    # Store data
                    from cloud_state_management import store_dataframe_in_cloud, update_state
                    from controllers import mark_stage_complete, go_to_stage
                    
                    success = store_dataframe_in_cloud(df, "main_data")
                    
                    if success:
                        update_state(
                            uploaded_filename=uploaded_file.name,
                            data_loaded=True
                        )
                        mark_stage_complete("upload")
                        st.success("Data uploaded successfully!")
                        st.balloons()
                        go_to_stage("ai_chat")
                    else:
                        st.error("Failed to store data. Please try again.")
                        
                except ImportError:
                    # Fallback for simple deployment
                    st.session_state.uploaded_data = df
                    st.session_state.uploaded_filename = uploaded_file.name
                    st.session_state.data_loaded = True
                    st.success("Data uploaded successfully!")
                    from controllers import mark_stage_complete, go_to_stage
                    mark_stage_complete("upload")
                    go_to_stage("ai_chat")
                    
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            st.info("Please check your file format and try again.")
    
    else:
        st.info("👆 Please upload a CSV or Excel file to get started.")
        
        # Sample data option
        if st.button("🎯 Use Sample Data", help="Load sample business data for testing"):
            # Create sample data
            sample_data = pd.DataFrame({
                'Company': ['Tech Corp A', 'Manufacturing B', 'Retail C', 'Services D', 'Tech Corp E'],
                'Industry': ['Technology', 'Manufacturing', 'Retail', 'Professional Services', 'Technology'],
                'Revenue': [1000000, 5000000, 2500000, 800000, 1500000],
                'Employees': [50, 200, 100, 25, 75],
                'Location': ['San Francisco', 'Detroit', 'Chicago', 'New York', 'Austin'],
                'Founded': [2015, 1995, 2008, 2010, 2018]
            })
            
            # Store sample data
            try:
                from cloud_state_management import store_dataframe_in_cloud, update_state
                from controllers import mark_stage_complete, go_to_stage
                
                success = store_dataframe_in_cloud(sample_data, "main_data")
                if success:
                    update_state(
                        uploaded_filename="sample_business_data.csv",
                        data_loaded=True
                    )
                    mark_stage_complete("upload")
                    st.success("Sample data loaded successfully!")
                    go_to_stage("ai_chat")
                    
            except ImportError:
                st.session_state.uploaded_data = sample_data
                st.session_state.uploaded_filename = "sample_business_data.csv"
                st.session_state.data_loaded = True
                from controllers import mark_stage_complete, go_to_stage
                mark_stage_complete("upload")
                st.success("Sample data loaded!")
                go_to_stage("ai_chat")