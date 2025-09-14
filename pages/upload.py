"""
Upload Page
===========
File upload interface with data filtering and download functionality.
"""
import streamlit as st
import pandas as pd
from datetime import datetime


def render():
    """Render the upload page."""
    from utils.layout import render_header
    from utils.winwood_styling import apply_winwood_theme
    
    apply_winwood_theme()
    render_header("📤 Upload Data", "Upload your CSV or Excel file with automatic preprocessing and filtering for business research")
    
    # Check current state
    try:
        from state_management import get_state
        state = get_state()
        data_loaded = state.data_loaded if hasattr(state, 'data_loaded') else False
        filename = state.uploaded_filename if hasattr(state, 'uploaded_filename') else ""
    except:
        # Fallback to session state
        data_loaded = st.session_state.get('data_loaded', False)
        filename = st.session_state.get('uploaded_filename', '')
    
    # Show current file info if any
    if data_loaded and filename:
        st.success(f"✅ Currently loaded: {filename}")
        
        # Show data info if available
        try:
            from state_management import get_state
            state = get_state()
            if hasattr(state, 'main_dataframe') and state.main_dataframe is not None:
                df = state.main_dataframe
                st.info(f"📊 Data Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
        except:
            # Try session state fallback
            if 'uploaded_data' in st.session_state and st.session_state.uploaded_data is not None:
                df = st.session_state.uploaded_data
                st.info(f"📊 Data Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    
    # File uploader - supports both CSV and XLSX
    uploaded_file = st.file_uploader(
        "Choose a CSV or Excel file",
        type=["csv", "xlsx"],
        help="Upload a CSV or Excel (.xlsx) file containing business contact data"
    )
    
    # Handle file upload
    if uploaded_file is not None:
        try:
            # Load data based on file type
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
                file_type = "CSV"
            else:
                df = pd.read_excel(uploaded_file)
                file_type = "Excel (.xlsx)"
            
            # Display basic info
            st.success(f"✅ Successfully loaded {file_type} file: {uploaded_file.name}")
            st.info(f"📊 Data Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
            
            # Show data preview
            st.subheader("📋 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Column information
            st.subheader("📊 Column Information")
            col_info = pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes,
                'Non-Null Count': df.count(),
                'Null Count': df.isnull().sum(),
                'Sample Values': [', '.join(df[col].dropna().astype(str).unique()[:3]) if len(df[col].dropna()) > 0 else 'No data' for col in df.columns]
            })
            st.dataframe(col_info, use_container_width=True)
            
            # Data filtering section
            st.subheader("🔍 Data Filtering (Optional)")
            
            # Find categorical columns for filtering
            categorical_columns = []
            for col in df.columns:
                if df[col].dtype == 'object':
                    unique_count = df[col].nunique()
                    if 2 <= unique_count <= 50:  # Good for filtering
                        categorical_columns.append(col)
            
            if categorical_columns:
                # Primary filter
                col1, col2 = st.columns(2)
                
                with col1:
                    filter_column = st.selectbox(
                        "Select column to filter by:",
                        ["None"] + categorical_columns,
                        help="Choose a categorical column to filter your data"
                    )
                
                with col2:
                    filter_values = []
                    if filter_column != "None":
                        unique_values = sorted(df[filter_column].dropna().unique())
                        filter_values = st.multiselect(
                            f"Select {filter_column} values:",
                            unique_values,
                            help=f"Choose specific values from {filter_column} to include"
                        )
                
                # Apply filters and show results
                filtered_df = df.copy()
                filter_applied = False
                
                if filter_column != "None" and filter_values:
                    filtered_df = df[df[filter_column].isin(filter_values)]
                    filter_applied = True
                    
                    # Show filter results
                    original_rows = len(df)
                    filtered_rows = len(filtered_df)
                    retention_rate = (filtered_rows / original_rows * 100) if original_rows > 0 else 0
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Original Rows", f"{original_rows:,}")
                    with col2:
                        st.metric("Filtered Rows", f"{filtered_rows:,}")
                    with col3:
                        st.metric("Retention %", f"{retention_rate:.1f}%")
                    
                    if filtered_rows > 0:
                        st.success(f"✅ Filter applied successfully!")
                        with st.expander("📋 Filtered Data Preview"):
                            st.dataframe(filtered_df.head(10), use_container_width=True)
                    else:
                        st.warning("⚠️ No data matches the current filters.")
                        filtered_df = df  # Reset to original
                        filter_applied = False
                
                final_df = filtered_df
            else:
                st.info("ℹ️ No suitable categorical columns found for filtering (need 2-50 unique values)")
                final_df = df
                filter_applied = False
            
            # Data quality checks
            st.subheader("🔍 Data Quality Checks")
            
            # Check for company/business name columns
            company_columns = []
            for col in df.columns:
                if any(keyword in col.lower() for keyword in ['name', 'company', 'consignee', 'business', 'customer', 'client']):
                    company_columns.append(col)
            
            if company_columns:
                st.success(f"✅ Company name columns found: {', '.join(company_columns)}")
                
                # Check for potential contact columns
                contact_columns = []
                for col in df.columns:
                    if any(keyword in col.lower() for keyword in ['email', 'phone', 'contact', 'website']):
                        contact_columns.append(col)
                
                if contact_columns:
                    st.info(f"📞 Contact columns detected: {', '.join(contact_columns)}")
                else:
                    st.warning("⚠️ No existing contact columns found - perfect for AI research!")
            else:
                st.warning("⚠️ No obvious company name columns detected. Please ensure your data has company/business names.")
            
            # Store data and proceed
            if st.button("✅ Confirm Upload & Continue", type="primary", use_container_width=True):
                try:
                    # Try to store using state management
                    from state_management import get_state, update_state
                    
                    # Store the data
                    if hasattr(get_state(), 'main_dataframe'):
                        # Update state management
                        state = get_state()
                        state.main_dataframe = final_df
                        state.original_dataframe = df  # Keep original for reference
                        update_state(
                            uploaded_filename=uploaded_file.name,
                            data_loaded=True
                        )
                    else:
                        # Fallback to session state
                        st.session_state.uploaded_data = final_df
                        st.session_state.original_data = df
                        st.session_state.uploaded_filename = uploaded_file.name
                        st.session_state.data_loaded = True
                    
                    # Also store in working data for consistency
                    st.session_state.working_data = final_df
                    
                    # Mark stage complete
                    from controllers import mark_stage_complete, go_to_stage
                    mark_stage_complete("upload")
                    
                    # Show success and navigate
                    filter_text = " (filtered)" if filter_applied else ""
                    st.success(f"🎉 Data uploaded successfully{filter_text}!")
                    st.balloons()
                    
                    # Navigate to next stage
                    go_to_stage("ai_chat")
                    
                except Exception as e:
                    st.error(f"❌ Error storing data: {str(e)}")
                    
                    # Fallback storage
                    st.session_state.uploaded_data = final_df
                    st.session_state.original_data = df
                    st.session_state.uploaded_filename = uploaded_file.name
                    st.session_state.data_loaded = True
                    st.session_state.working_data = final_df
                    
                    st.success("✅ Data stored in fallback mode")
                    
                    # Navigate using fallback
                    st.session_state.current_stage = "ai_chat"
                    st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            st.info("Please check your file format and try again.")
    
    else:
        # Show upload instructions when no file is uploaded
        st.info("👆 Please upload a CSV or Excel file to get started.")
        
        # Enhanced file format info
        with st.expander("📋 File Format Requirements & Features"):
            st.write("""
            **Supported File Types:**
            - **CSV files** (.csv): Direct upload and processing
            - **Excel files** (.xlsx): Automatically processed
            
            **AI-Powered Business Research Features:**
            🔍 **Smart Contact Discovery**: Find emails, phones, and websites for companies
            🤖 **AI-Enhanced Research**: Uses Tavily + Groq for accurate business intelligence
            📊 **Data Filtering**: Filter by any categorical column before research
            📧 **Email Outreach**: Generate and send personalized business emails
            
            **For best results, your file should contain:**
            - Header row with column names
            - **Company/Business name column** (required for research)
            - Location data (City, Country) for better accuracy
            - Any existing contact data (optional - AI will enhance)
            
            **Example Structure:**
            ```
            Consignee Name,City,Country,Product,Value
            ABC Timber Co,Mumbai,India,Teak Wood,25000
            XYZ Lumber Ltd,Delhi,India,Pine Lumber,18000
            Global Wood Inc,Chennai,India,Plywood,30000
            ```
            
            **Complete Workflow:**
            1. **📤 Upload & Filter**: Upload data → Apply optional filters
            2. **🤖 AI Chat**: Interact with AI about your data
            3. **📊 Visualizations**: Explore data with interactive charts
            4. **🔍 Business Research**: AI-powered contact discovery
            5. **📧 Email Outreach**: Send personalized campaigns
            """)
        
        # Sample data option
        if st.button("🎯 Use Sample Timber Business Data", help="Load sample data for testing"):
            # Create comprehensive sample data
            sample_data = pd.DataFrame({
                'Consignee Name': [
                    'Acme Timber Corporation',
                    'Global Wood Solutions', 
                    'Teakwood Trading Inc',
                    'Premium Lumber LLC',
                    'Forest Products Co',
                    'Mumbai Wood Industries',
                    'Chennai Timber Exports',
                    'Bangalore Furniture Co'
                ],
                'Consignee City': [
                    'Mumbai', 'Delhi', 'Chennai', 'Bangalore', 
                    'Kolkata', 'Mumbai', 'Chennai', 'Bangalore'
                ],
                'Country': [
                    'India', 'India', 'India', 'India',
                    'India', 'India', 'India', 'India'
                ],
                'Product': [
                    'Teak Wood', 'Plywood', 'Timber Logs', 'Lumber',
                    'Wood Panels', 'Furniture Wood', 'Export Timber', 'Wooden Furniture'
                ],
                'Quantity': [100, 200, 150, 300, 75, 120, 180, 90],
                'Value_USD': [10000, 25000, 18000, 45000, 8500, 15000, 22000, 12000],
                'HS_Code': ['44011200', '44121000', '44031100', '44071000', '44181000', '44031200', '44011100', '44091200']
            })
            
            # Store sample data
            try:
                from state_management import get_state, update_state
                state = get_state()
                if hasattr(state, 'main_dataframe'):
                    state.main_dataframe = sample_data
                    update_state(
                        uploaded_filename="sample_timber_data.csv",
                        data_loaded=True
                    )
                else:
                    st.session_state.uploaded_data = sample_data
                    st.session_state.uploaded_filename = "sample_timber_data.csv"
                    st.session_state.data_loaded = True
                
                st.session_state.working_data = sample_data
                
                # Mark upload complete and navigate
                from controllers import mark_stage_complete, go_to_stage
                mark_stage_complete("upload")
                st.success("✅ Sample timber business data loaded!")
                go_to_stage("ai_chat")
                
            except Exception as e:
                # Fallback
                st.session_state.uploaded_data = sample_data
                st.session_state.uploaded_filename = "sample_timber_data.csv"
                st.session_state.data_loaded = True
                st.session_state.working_data = sample_data
                st.session_state.current_stage = "ai_chat"
                st.success("✅ Sample data loaded!")
                st.rerun()


if __name__ == "__main__":
    render()