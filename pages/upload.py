"""
Upload Page
===========
File upload and data processing page.
"""
import streamlit as st
import pandas as pd
from utils.layout import (
    render_file_upload_area, 
    render_dataframe_preview, 
    show_success_message, 
    show_error_message,
    create_download_section
)


def render():
    """Render the upload page."""
    st.title("📤 Upload Your Data")
    st.markdown("Upload your business data to get started with research and analysis.")
    
    # File upload area
    uploaded_file = render_file_upload_area()
    
    if uploaded_file is not None:
        try:
            # Handle file upload
            from controllers import handle_file_upload
            success = handle_file_upload(uploaded_file)
            
            if success:
                # Get uploaded data
                try:
                    from state_management import get_state
                    state = get_state()
                    df = state.main_dataframe
                    
                    if df is not None and not df.empty:
                        # Show data preview
                        render_dataframe_preview(df, "Uploaded Data Preview")
                        
                        # Create download section
                        create_download_section(df, "uploaded_data")
                        
                        # Show proceed button
                        st.markdown("---")
                        col1, col2 = st.columns([1, 2])
                        
                        with col2:
                            if st.button("🚀 Proceed to Web Research", type="primary", use_container_width=True):
                                from controllers import proceed_to_web_research
                                proceed_to_web_research()
                    
                except Exception as e:
                    show_error_message("Error accessing uploaded data", str(e))
            
        except ImportError:
            # Fallback if controllers not available
            show_error_message("Upload functionality not available", "Required modules not found")
        except Exception as e:
            show_error_message("Upload failed", str(e))
    
    else:
        # Show instructions
        st.markdown("""
        ### Instructions:
        1. **Upload your data file** (CSV or Excel format)
        2. **Review the data preview** to ensure it loaded correctly
        3. **Proceed to Web Research** to enhance your data with business information
        
        ### Supported Formats:
        - **CSV files** (.csv)
        - **Excel files** (.xlsx, .xls)
        
        ### Tips:
        - Ensure your file has proper headers in the first row
        - Keep file size under 50MB for optimal performance
        - Make sure business names are in a clearly labeled column
        """)
        
        # Show sample data format
        with st.expander("📋 Sample Data Format"):
            sample_data = pd.DataFrame({
                'Company Name': ['ABC Corp', 'XYZ Ltd', 'Tech Solutions Inc'],
                'Industry': ['Manufacturing', 'Retail', 'Technology'],
                'Location': ['New York', 'California', 'Texas'],
                'Contact Email': ['info@abc.com', 'sales@xyz.com', 'hello@tech.com']
            })
            st.dataframe(sample_data, use_container_width=True)
            st.caption("Example of a properly formatted data file")


if __name__ == "__main__":
    render()
