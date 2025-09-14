"""
Business Research Page
=====================
Main business research and mapping functionality.
"""

import streamlit as st
import pandas as pd


def enhanced_business_research_page():
    """Enhanced business research page."""
    from utils.layout import render_header
    from utils.winwood_styling import apply_winwood_theme
    
    apply_winwood_theme()
    render_header("🗺️ Business Research", "Advanced business intelligence and mapping")
    
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
    
    # Business research interface
    st.subheader("🔍 Business Research Tools")
    
    # Research options
    research_type = st.selectbox(
        "Select research type:",
        [
            "Company Analysis",
            "Market Research", 
            "Competitive Intelligence",
            "Industry Trends",
            "Geographic Analysis"
        ]
    )
    
    if research_type == "Company Analysis":
        st.info("🏢 Company Analysis: Research individual companies in your dataset")
        
        # Company selection
        if 'Company' in df.columns:
            companies = df['Company'].unique().tolist()
            selected_company = st.selectbox("Select a company to research:", companies)
            
            if selected_company:
                company_data = df[df['Company'] == selected_company]
                st.subheader(f"Analysis for {selected_company}")
                st.dataframe(company_data, use_container_width=True)
                
                # Basic company metrics
                if len(company_data) > 0:
                    st.write("**Company Overview:**")
                    for col in company_data.columns:
                        if col != 'Company':
                            values = company_data[col].dropna().unique()
                            if len(values) > 0:
                                st.write(f"- {col}: {', '.join(map(str, values))}")
        else:
            st.warning("No 'Company' column found in the data. Please ensure your data has a company identifier column.")
    
    elif research_type == "Geographic Analysis":
        st.info("🗺️ Geographic Analysis: Analyze business locations and territories")
        
        # Location analysis
        location_cols = [col for col in df.columns if any(keyword in col.lower() for keyword in ['location', 'city', 'state', 'country', 'address'])]
        
        if location_cols:
            selected_location_col = st.selectbox("Select location column:", location_cols)
            
            if selected_location_col:
                location_counts = df[selected_location_col].value_counts()
                st.subheader(f"Business Distribution by {selected_location_col}")
                st.bar_chart(location_counts.head(20))
                
                # Location details
                st.subheader("Location Breakdown")
                st.dataframe(location_counts.head(20), use_container_width=True)
        else:
            st.warning("No location columns found. Please ensure your data includes location information.")
    
    elif research_type == "Industry Trends":
        st.info("📈 Industry Trends: Analyze industry patterns and trends")
        
        # Industry analysis
        industry_cols = [col for col in df.columns if any(keyword in col.lower() for keyword in ['industry', 'sector', 'category', 'type'])]
        
        if industry_cols:
            selected_industry_col = st.selectbox("Select industry column:", industry_cols)
            
            if selected_industry_col:
                industry_counts = df[selected_industry_col].value_counts()
                st.subheader(f"Distribution by {selected_industry_col}")
                st.bar_chart(industry_counts)
                
                # Industry insights
                st.subheader("Industry Insights")
                st.dataframe(industry_counts, use_container_width=True)
        else:
            st.warning("No industry columns found. Please ensure your data includes industry classification.")
    
    else:
        st.info(f"🔍 {research_type}: This feature provides advanced business intelligence capabilities")
        st.write("This is a placeholder for advanced research functionality. The full version includes:")
        st.write("• Real-time company data enrichment")
        st.write("• Market analysis and competitive intelligence")
        st.write("• Industry trend analysis")
        st.write("• Geographic mapping and territory analysis")
        st.write("• Contact discovery and verification")
    
    # Research actions
    st.subheader("🚀 Research Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Deep Research", help="Perform comprehensive research on selected data"):
            st.info("Deep research functionality would be activated here")
    
    with col2:
        if st.button("📊 Generate Report", help="Create a detailed research report"):
            st.info("Report generation would be triggered here")
    
    with col3:
        if st.button("💾 Export Results", help="Export research findings"):
            st.info("Export functionality would be available here")
    
    # Navigation
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("← Visualizations", use_container_width=True):
            from controllers import go_to_stage
            go_to_stage("visualizations")
    
    with col2:
        if st.button("📧 Email Outreach", use_container_width=True):
            from controllers import go_to_stage
            go_to_stage("analyze")
    
    with col3:
        if st.button("📁 Back to Upload", use_container_width=True):
            from controllers import go_to_stage
            go_to_stage("upload")